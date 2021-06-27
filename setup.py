from os import path

from jupyter_packaging import (
    combine_commands,
    create_cmdclass,
    ensure_python,
    ensure_targets,
    get_version,
    install_npm,
)
from setuptools import find_packages, setup

ensure_python(("2.7", ">=3.7"))
pjoin = path.join
name = "ipydagred3"
here = path.abspath(path.dirname(__file__))
jshere = path.abspath(pjoin(path.dirname(__file__), "js"))
version = get_version(pjoin(here, name, "_version.py"))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read().replace("\r\n", "\n")

requires = ["ipywidgets>=7.5.1"]

requires_dev = requires + [
    "black>=20.",
    "bump2version>=1.0.0",
    "flake8>=3.7.8",
    "flake8-black>=0.2.1",
    "jupyter_packaging",
    "mock",
    "pytest>=4.3.0",
    "pytest-cov>=2.6.1",
    "Sphinx>=1.8.4",
    "sphinx-markdown-builder>=0.5.2",
]

nb_path = pjoin(here, name, "nbextension", "static")
lab_path = pjoin(here, name, "labextension")

# Representative files that should exist after a successful build
jstargets = [
    pjoin(jshere, "lib", "index.js"),
]

package_data_spec = {name: ["nbextension/static/*.*js*", "labextension/*.tgz"]}

data_files_spec = [
    ("share/jupyter/nbextensions/ipydagred3", nb_path, "*.js*"),
    ("share/jupyter/lab/extensions", lab_path, "*.tgz"),
    ("etc/jupyter/nbconfig/notebook.d", here, "ipydagred3.json"),
]


cmdclass = create_cmdclass(
    "jsdeps", package_data_spec=package_data_spec, data_files_spec=data_files_spec
)
cmdclass["jsdeps"] = combine_commands(
    install_npm(jshere, build_cmd="build:all"),
    ensure_targets(jstargets),
)


setup(
    name=name,
    version=version,
    description="ipywidgets wrapper around dagre-d3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/timkpaine/ipydagred3",
    author="Tim Paine",
    author_email="t.paine154@gmail.com",
    license="Apache 2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Jupyter",
    ],
    platforms="Linux, Mac OS X, Windows",
    keywords=["Jupyter", "Jupyterlab", "Widgets", "IPython", "Graph", "Data", "DAG"],
    cmdclass=cmdclass,
    packages=find_packages(
        exclude=[
            "tests",
        ]
    ),
    install_requires=requires,
    extras_require={"dev": requires_dev},
    include_package_data=True,
    data_files=[
        (
            "share/jupyter/nbextensions/ipydagred3",
            [
                "ipydagred3/nbextension/static/extension.js",
                "ipydagred3/nbextension/static/index.js",
                "ipydagred3/nbextension/static/index.js.map",
            ],
        ),
        ("etc/jupyter/nbconfig/notebook.d", ["ipydagred3.json"]),
    ],
    zip_safe=False,
)
