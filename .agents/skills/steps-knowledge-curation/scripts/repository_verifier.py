"""Resolve the verifier from the STEPS checkout regardless of loaded packages."""

from importlib.util import module_from_spec, spec_from_file_location

from register_paths import REPOSITORY_ROOT

_path = REPOSITORY_ROOT / "scripts" / "verify_reference_integrity.py"
_spec = spec_from_file_location("_steps_curation_repository_verifier", _path)
if _spec is None or _spec.loader is None:
    raise ImportError(f"Cannot load the STEPS repository verifier: {_path}")
verifier = module_from_spec(_spec)
_spec.loader.exec_module(verifier)
