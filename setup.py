from setuptools import setup, find_packages
from typing import List

def get_requirements()->List[str]:
    
    '''
    This function returns a list of requirements
    
    '''
    requirement_lst:List[str]=[]
    
    try:
        with open('requirements.txt', 'r') as file:
            lines=file.readlines()
            
            for line in lines:
                requirement=line.strip()
                if requirement and requirement.strip() != '-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print('Requirements file not found')
    
    return requirement_lst

setup(
    name='NetworkSecurity',
    version='0.0.1',
    packages=find_packages(),
    install_requires=get_requirements(),
    author='Momen Walied',
    author_email='momenwalied2002@gmail.com',
)