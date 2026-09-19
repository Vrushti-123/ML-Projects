from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = '-e .'
def get_requirements(file_path: str)->List[str]:
    '''this function will return a list of requirements'''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

    return requirements


# basically metadata of the project.
setup(
    name="mlproject",
    version="0.0.1",
    author="Vrushti",
    author_email="vrushtip2006@gmail.com",
    packages=find_packages(),
    # install_requires=['pandas', 'numpy', 'seaborn']
    install_requires=get_requirements("requirements.txt")
    # automatically install these libraries when installing the package
)