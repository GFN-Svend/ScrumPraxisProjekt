import importlib
import importlib.metadata
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS_FILE = PROJECT_ROOT / "requirements.txt"


class DependencyTest(unittest.TestCase):
    def get_pinned_dependencies(self) -> list[tuple[str, str]]:
        dependencies = []

        for raw_line in REQUIREMENTS_FILE.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            self.assertIn(
                "==",
                line,
                msg=f"Abhängigkeit muss exakt versioniert sein: {line}",
            )
            package_name, expected_version = line.split("==", maxsplit=1)
            dependencies.append((package_name, expected_version))

        return dependencies

    def test_requirements_are_installed_in_pinned_versions(self) -> None:
        for package_name, expected_version in self.get_pinned_dependencies():
            with self.subTest(package=package_name):
                installed_version = importlib.metadata.version(package_name)
                self.assertEqual(installed_version, expected_version)

    def test_direct_dependencies_are_importable(self) -> None:
        for package_name, _expected_version in self.get_pinned_dependencies():
            with self.subTest(package=package_name):
                import_name = package_name.lower().replace("-", "_")
                importlib.import_module(import_name)


if __name__ == "__main__":
    unittest.main()
