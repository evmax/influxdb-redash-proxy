# coding: utf-8
from os.path import abspath
from os.path import dirname
from os.path import join
import re

from pkg_resources import Requirement
from setuptools import find_packages
from setuptools import setup


_COMMENT_RE = re.compile(r'(^|\s)+#.*$')


def _get_requirements(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            line = _COMMENT_RE.sub('', line)
            line = line.strip()
            if line.startswith('-r '):
                yield from _get_requirements(
                    join(dirname(abspath(file_path)), line[3:])
                )
            elif line:
                req = Requirement(line)
                req_str = f'{req.name}{req.specifier}'
                if req.marker:
                    req_str += f'; {req.marker}'
                yield req_str


def _read(file_name):
    with open(file_name, 'r') as infile:
        return infile.read()


def main():
    setup(
        name="influxdb_proxy",
        version="0.0.1",
        url='https://',
        author="Max Elakhov",
        author_email='',
        description=_read('DESCRIPTION'),
        keywords="flask",
        packages=find_packages('src'),
        package_dir={'': 'src'},
        include_package_data=True,
        install_requires=tuple(_get_requirements('requirements/prod.txt')),
        zip_safe=False,
        set_build_info=join(dirname(__file__), 'src', 'webhook_proxy'),
    )


if __name__ == '__main__':
    main()
