import argparse
import json
import shlex
import statistics
import subprocess
import sys
import tempfile
import time
from dataclasses import asdict, dataclass
from pathlib import Path

sys.path.extend([".", ".."])

import pyfiglet
from loguru import logger
from pycparser import c_generator, c_parser

from src.directive import DirectiveParser
from src.selfcaller import SelfCallHiddenAdder


@dataclass
class BenchmarkSummary:
    runs: int
    baseline_compile_avg: float
    baseline_compile_std: float
    preprocess_avg: float
    preprocess_std: float
    transformed_compile_avg: float
    transformed_compile_std: float
    transformed_total_avg: float
    transformed_total_std: float
    delta_total_avg: float
    delta_total_pct: float
    delta_compile_only_avg: float
    delta_compile_only_pct: float


def _mean_std(values: list[float]) -> tuple[float, float]:
    if not values:
        return 0.0, 0.0
    if len(values) == 1:
        return values[0], 0.0
    return statistics.fmean(values), statistics.stdev(values)


def _summarize(
    baseline_runs: list[float],
    preprocess_runs: list[float],
    transformed_compile_runs: list[float],
) -> BenchmarkSummary:
    transformed_total_runs = [
        p + c for p, c in zip(preprocess_runs, transformed_compile_runs)
    ]

    baseline_avg, baseline_std = _mean_std(baseline_runs)
    preprocess_avg, preprocess_std = _mean_std(preprocess_runs)
    transformed_compile_avg, transformed_compile_std = _mean_std(transformed_compile_runs)
    transformed_total_avg, transformed_total_std = _mean_std(transformed_total_runs)

    delta_total_avg = transformed_total_avg - baseline_avg
    delta_compile_only_avg = transformed_compile_avg - baseline_avg

    delta_total_pct = (
        (delta_total_avg / baseline_avg) * 100.0 if baseline_avg > 0 else 0.0
    )
    delta_compile_only_pct = (
        (delta_compile_only_avg / baseline_avg) * 100.0 if baseline_avg > 0 else 0.0
    )

    return BenchmarkSummary(
        runs=len(baseline_runs),
        baseline_compile_avg=baseline_avg,
        baseline_compile_std=baseline_std,
        preprocess_avg=preprocess_avg,
        preprocess_std=preprocess_std,
        transformed_compile_avg=transformed_compile_avg,
        transformed_compile_std=transformed_compile_std,
        transformed_total_avg=transformed_total_avg,
        transformed_total_std=transformed_total_std,
        delta_total_avg=delta_total_avg,
        delta_total_pct=delta_total_pct,
        delta_compile_only_avg=delta_compile_only_avg,
        delta_compile_only_pct=delta_compile_only_pct,
    )


def _load_symtable(path: Path) -> tuple[dict, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["symtab"], data["struct_graph"]


def _save_symtable(path: Path, symtab: dict, struct_graph: dict) -> None:
    payload = {
        "symtab": symtab,
        "struct_graph": struct_graph,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _gcc_preprocess_code(include_dirs: list[str], cpp_args: list[str], code: str) -> str:
    tmp = tempfile.NamedTemporaryFile(suffix=".i", delete=False)
    tmp_path = Path(tmp.name)
    tmp.close()

    try:
        cmd = [
            "gcc",
            "-E",
            "-P",
            "-nostdinc",
            *cpp_args,
        ]

        for include_dir in include_dirs:
            cmd.append(f"-I{include_dir}")

        cmd.append("-Imisc/pycparser_fake_libs")
        cmd += ["-", "-o", str(tmp_path)]

        completed = subprocess.run(
            cmd,
            input=code.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        if completed.returncode != 0:
            raise RuntimeError(
                "gcc -E failed\n"
                f"Command: {' '.join(cmd)}\n"
                f"stderr:\n{completed.stderr.decode('utf-8', errors='replace')}"
            )

        return tmp_path.read_text(encoding="utf-8")
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def _compile_path(
    source_path: Path,
    compiler: str,
    include_dirs: list[str],
    cpp_args: list[str],
    cflags: list[str],
    mode: str,
) -> float:
    obj_tmp = tempfile.NamedTemporaryFile(suffix=".o", delete=False)
    obj_path = Path(obj_tmp.name)
    obj_tmp.close()

    try:
        cmd = [compiler, *cpp_args, *cflags]
        for include_dir in include_dirs:
            cmd.append(f"-I{include_dir}")

        if mode == "syntax":
            cmd += ["-fsyntax-only", str(source_path)]
        elif mode == "object":
            cmd += ["-c", str(source_path), "-o", str(obj_path)]
        else:
            raise ValueError(f"Unknown mode: {mode}")

        t0 = time.perf_counter()
        completed = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        elapsed = time.perf_counter() - t0

        if completed.returncode != 0:
            raise RuntimeError(
                "Compilation failed\n"
                f"Command: {' '.join(cmd)}\n"
                f"stderr:\n{completed.stderr.decode('utf-8', errors='replace')}"
            )

        return elapsed
    finally:
        if obj_path.exists():
            obj_path.unlink()


def _compile_code(
    code: str,
    compiler: str,
    cflags: list[str],
    mode: str,
) -> float:
    src_tmp = tempfile.NamedTemporaryFile(suffix=".c", delete=False, mode="w", encoding="utf-8")
    src_tmp.write(code)
    src_tmp.flush()
    src_path = Path(src_tmp.name)
    src_tmp.close()

    try:
        return _compile_path(
            source_path=src_path,
            compiler=compiler,
            include_dirs=[],
            cpp_args=[],
            cflags=cflags,
            mode=mode,
        )
    finally:
        if src_path.exists():
            src_path.unlink()


def _collect_global_symbols(directory: Path) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    global_symtab: dict[str, list[str]] = {}
    global_graph: dict[str, list[str]] = {}

    for path in sorted(directory.rglob("*")):
        if path.suffix.lower() not in (".c", ".h"):
            continue

        source = path.read_text(encoding="utf-8")
        processor = DirectiveParser(source)
        symtab, struct_graph = processor.build_symtable()

        global_symtab.update(symtab)

        for key, values in struct_graph.items():
            if key not in global_graph:
                global_graph[key] = []
            global_graph[key].extend(values)

    return global_symtab, global_graph


def _transform_source(
    source_text: str,
    include_dirs: list[str],
    cpp_args: list[str],
    symtab: dict | None = None,
    struct_graph: dict | None = None,
) -> tuple[str, float, dict, dict]:
    t0 = time.perf_counter()

    processor = DirectiveParser(source_text)

    if symtab is None or struct_graph is None:
        symtab, struct_graph = processor.build_symtable()

    processed_code = processor.process_code()
    preprocessed = _gcc_preprocess_code(include_dirs, cpp_args, processed_code)

    cparser = c_parser.CParser()
    ast = cparser.parse(preprocessed)

    visitor = SelfCallHiddenAdder(symtab=symtab, struct_graph=struct_graph)
    visitor.visit(ast)

    generator = c_generator.CGenerator()
    generated_code = generator.visit(ast)

    elapsed = time.perf_counter() - t0
    return generated_code, elapsed, symtab, struct_graph


def _dump_transformed_file(
    dump_root: Path,
    original_path: Path,
    transformed_code: str,
    base_dir: Path | None = None,
) -> None:
    if base_dir is None:
        dump_path = dump_root
    else:
        relative = original_path.relative_to(base_dir)
        dump_path = dump_root / relative
        dump_path = dump_path.with_suffix(".selfcall.c")

    dump_path.parent.mkdir(parents=True, exist_ok=True)
    dump_path.write_text(transformed_code, encoding="utf-8")


def _benchmark_file(
    source_path: Path,
    include_dirs: list[str],
    cpp_args: list[str],
    compiler: str,
    cflags: list[str],
    mode: str,
    repeat: int,
    loaded_symtab: dict | None = None,
    loaded_graph: dict | None = None,
    dump_transformed: Path | None = None,
) -> BenchmarkSummary:
    source_text = source_path.read_text(encoding="utf-8")

    baseline_runs: list[float] = []
    preprocess_runs: list[float] = []
    transformed_compile_runs: list[float] = []

    for run_idx in range(repeat):
        def _run_baseline() -> float:
            return _compile_path(
                source_path=source_path,
                compiler=compiler,
                include_dirs=include_dirs,
                cpp_args=cpp_args,
                cflags=cflags,
                mode=mode,
            )

        def _run_transformed() -> tuple[float, float]:
            transformed_code, preprocess_time, _, _ = _transform_source(
                source_text=source_text,
                include_dirs=include_dirs,
                cpp_args=cpp_args,
                symtab=loaded_symtab,
                struct_graph=loaded_graph,
            )

            if dump_transformed is not None and run_idx == 0:
                _dump_transformed_file(
                    dump_root=dump_transformed,
                    original_path=source_path,
                    transformed_code=transformed_code,
                    base_dir=None,
                )

            transformed_compile_time = _compile_code(
                code=transformed_code,
                compiler=compiler,
                cflags=cflags,
                mode=mode,
            )
            return preprocess_time, transformed_compile_time

        if run_idx % 2 == 0:
            baseline = _run_baseline()
            preprocess_time, transformed_compile = _run_transformed()
        else:
            preprocess_time, transformed_compile = _run_transformed()
            baseline = _run_baseline()

        baseline_runs.append(baseline)
        preprocess_runs.append(preprocess_time)
        transformed_compile_runs.append(transformed_compile)

    return _summarize(baseline_runs, preprocess_runs, transformed_compile_runs)


def _benchmark_directory(
    directory: Path,
    include_dirs: list[str],
    cpp_args: list[str],
    compiler: str,
    cflags: list[str],
    mode: str,
    repeat: int,
    loaded_symtab: dict | None = None,
    loaded_graph: dict | None = None,
    dump_transformed: Path | None = None,
) -> BenchmarkSummary:
    sources = sorted(p for p in directory.rglob("*.c"))
    if not sources:
        raise RuntimeError(f"No .c files found in: {directory}")

    baseline_runs: list[float] = []
    preprocess_runs: list[float] = []
    transformed_compile_runs: list[float] = []

    for run_idx in range(repeat):
        def _run_baseline_all() -> float:
            total = 0.0
            for src in sources:
                total += _compile_path(
                    source_path=src,
                    compiler=compiler,
                    include_dirs=include_dirs,
                    cpp_args=cpp_args,
                    cflags=cflags,
                    mode=mode,
                )
            return total

        def _run_transformed_all() -> tuple[float, float]:
            preprocess_total = 0.0
            transformed_compile_total = 0.0

            if loaded_symtab is None or loaded_graph is None:
                t0 = time.perf_counter()
                symtab, graph = _collect_global_symbols(directory)
                preprocess_total += time.perf_counter() - t0
            else:
                symtab, graph = loaded_symtab, loaded_graph

            for src in sources:
                source_text = src.read_text(encoding="utf-8")

                transformed_code, preprocess_time, _, _ = _transform_source(
                    source_text=source_text,
                    include_dirs=include_dirs,
                    cpp_args=cpp_args,
                    symtab=symtab,
                    struct_graph=graph,
                )
                preprocess_total += preprocess_time

                if dump_transformed is not None and run_idx == 0:
                    _dump_transformed_file(
                        dump_root=dump_transformed,
                        original_path=src,
                        transformed_code=transformed_code,
                        base_dir=directory,
                    )

                transformed_compile_total += _compile_code(
                    code=transformed_code,
                    compiler=compiler,
                    cflags=cflags,
                    mode=mode,
                )

            return preprocess_total, transformed_compile_total

        if run_idx % 2 == 0:
            baseline = _run_baseline_all()
            preprocess_time, transformed_compile = _run_transformed_all()
        else:
            preprocess_time, transformed_compile = _run_transformed_all()
            baseline = _run_baseline_all()

        baseline_runs.append(baseline)
        preprocess_runs.append(preprocess_time)
        transformed_compile_runs.append(transformed_compile)

    return _summarize(baseline_runs, preprocess_runs, transformed_compile_runs)


def _print_summary(label: str, summary: BenchmarkSummary) -> None:
    logger.info(
        "\n"
        f"===== {label} =====\n"
        f"runs:                {summary.runs}\n"
        f"baseline compile:    {summary.baseline_compile_avg:.6f} s ± {summary.baseline_compile_std:.6f}\n"
        f"custom preprocess:   {summary.preprocess_avg:.6f} s ± {summary.preprocess_std:.6f}\n"
        f"transformed compile: {summary.transformed_compile_avg:.6f} s ± {summary.transformed_compile_std:.6f}\n"
        f"transformed total:   {summary.transformed_total_avg:.6f} s ± {summary.transformed_total_std:.6f}\n"
        f"delta total:         {summary.delta_total_avg:+.6f} s ({summary.delta_total_pct:+.2f}%)\n"
        f"delta compile only:  {summary.delta_compile_only_avg:+.6f} s ({summary.delta_compile_only_pct:+.2f}%)\n"
    )


if __name__ == "__main__":
    ascii_banner = pyfiglet.figlet_format("SelfCall benchmark!")
    print(ascii_banner)

    parser = argparse.ArgumentParser(
        description="Benchmark the impact of SelfCall preprocessing on total compilation time."
    )
    parser.add_argument("--file", default=None, help="Source C file for benchmarking")
    parser.add_argument("--directory", default=None, help="Source directory for benchmarking")
    parser.add_argument(
        "--include",
        action="append",
        default=[],
        help="Project include directory. Can be specified multiple times.",
    )
    parser.add_argument(
        "--symtable",
        default=None,
        help="Path to a saved symtable JSON. If passed, build_symtable time is excluded.",
    )
    parser.add_argument(
        "--save-symtab",
        nargs="?",
        const="symtable.json",
        default=None,
        help="Dump a built symtable to JSON. If no path is given, saves to ./symtable.json",
    )
    parser.add_argument(
        "--dump-transformed",
        default=None,
        help="For --file: path to transformed .c file. For --directory: directory for transformed files.",
    )
    parser.add_argument(
        "--compiler",
        default="gcc",
        help="Compiler executable used for baseline and transformed compilation",
    )
    parser.add_argument(
        "--cpp-args",
        default="",
        help='Extra preprocessor/frontend args, e.g. \'-DDEBUG=1 -Ithird_party/include\'',
    )
    parser.add_argument(
        "--cflags",
        default="-std=c11",
        help='Extra compiler flags, e.g. \'-O2 -Wall -Wextra\'',
    )
    parser.add_argument(
        "--mode",
        choices=("syntax", "object"),
        default="syntax",
        help="syntax = -fsyntax-only, object = -c",
    )
    parser.add_argument(
        "--repeat",
        type=int,
        default=5,
        help="How many benchmark runs to perform",
    )
    parser.add_argument(
        "--json-out",
        default=None,
        help="Write benchmark summary to JSON file",
    )

    args = parser.parse_args()

    if not args.file and not args.directory:
        logger.error("--file or --directory options are required!")
        raise SystemExit(1)

    if args.file and args.directory:
        logger.error("Use either --file or --directory, not both!")
        raise SystemExit(1)

    include_dirs = args.include or []
    cpp_args = shlex.split(args.cpp_args)
    cflags = shlex.split(args.cflags)

    loaded_symtab = None
    loaded_graph = None
    if args.symtable:
        loaded_symtab, loaded_graph = _load_symtable(Path(args.symtable))
        logger.info(f"Loaded symtable from: {args.symtable}")

    summary: BenchmarkSummary

    if args.file:
        src = Path(args.file)

        if args.save_symtab and not args.symtable:
            source_text = src.read_text(encoding="utf-8")
            processor = DirectiveParser(source_text)
            symtab, graph = processor.build_symtable()
            _save_symtable(Path(args.save_symtab), symtab, graph)
            logger.info(f"Symtable saved to: {args.save_symtab}")

        summary = _benchmark_file(
            source_path=src,
            include_dirs=include_dirs,
            cpp_args=cpp_args,
            compiler=args.compiler,
            cflags=cflags,
            mode=args.mode,
            repeat=args.repeat,
            loaded_symtab=loaded_symtab,
            loaded_graph=loaded_graph,
            dump_transformed=Path(args.dump_transformed) if args.dump_transformed else None,
        )
        _print_summary(f"FILE: {src}", summary)

    else:
        directory = Path(args.directory)

        if args.save_symtab and not args.symtable:
            symtab, graph = _collect_global_symbols(directory)
            _save_symtable(Path(args.save_symtab), symtab, graph)
            logger.info(f"Symtable saved to: {args.save_symtab}")

        summary = _benchmark_directory(
            directory=directory,
            include_dirs=include_dirs,
            cpp_args=cpp_args,
            compiler=args.compiler,
            cflags=cflags,
            mode=args.mode,
            repeat=args.repeat,
            loaded_symtab=loaded_symtab,
            loaded_graph=loaded_graph,
            dump_transformed=Path(args.dump_transformed) if args.dump_transformed else None,
        )
        _print_summary(f"DIRECTORY: {directory}", summary)

    if args.json_out:
        Path(args.json_out).write_text(
            json.dumps(asdict(summary), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        logger.info(f"Benchmark JSON saved to: {args.json_out}")