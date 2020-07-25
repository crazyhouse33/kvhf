import os
import pytest


prefix='PYTHONPATH=:../.. python3 ../../bin/done/done.py '

def check_stat(command_line, expected):
    assert os.WEXITSTATUS(os.system(command_line))== expected


def test_general():
    try:
        os.remove('a')
    except:
        pass
    createcmd='\'python3 -c "print(\\"a\\",file=open(\\"a\\",\\"w\\"))"\''
    #This is in a shell:
    #'python3 -c "print(\"a\",file=open(\"a\",\"w\"))"'

    check_stat(prefix + " -f .done init", 0)
    
    check_stat(prefix + 'exec  -r testaction pouet',1)
    check_stat(prefix + 'exec  -p testaction '+createcmd,0)
    assert os.path.isfile('a')
    os.remove('a')
    check_stat(prefix + 'exec  -p testaction "python -c print(a)"',2)

    check_stat(prefix +  'exec  -r testaction '+ createcmd + ' -l testaction',0)
    assert os.path.isfile('a')
    os.remove('a')
    check_stat(prefix + 'exec  -p testaction '+createcmd,0)
    assert not os.path.isfile('a')
    check_stat(prefix + 'exec  --lock-no-fail -p testaction '+createcmd,1)
    assert not os.path.isfile('a')
    check_stat(prefix + 'exec  --required-permissive -r aaaaa ' +createcmd,0)
    assert not os.path.isfile('a')
    
    check_stat(prefix + 'exec -p toto ',0)
    
    check_stat(prefix + 'exec -r toto ',0)
    check_stat(prefix + 'exec -p titi -a',0)
    check_stat(prefix + 'exec -p titi --lock-no-fail',1)
    check_stat(prefix + 'exec -r titi -a --lock-no-fail',0)
