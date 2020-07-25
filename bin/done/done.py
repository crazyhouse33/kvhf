import os
import sys
from lib.done import Done_file
import bin.done.parser as parser

def exit(msg, status):
    print(msg, file=sys.stderr)
    sys.exit(status)


def manage_command_ret(ret):
    print ('Exit status:', ret)
    if not child_permissive and ret !=0:
        exit('The given command failed with exit status ' +str(ret)+'.', 2)


def check_produced(actions):
    locked=done_file.locked(actions)
    if locked:
        exit_status= int(lock_no_fail)
        exit('The following are allready done but locked:\n'+'\n'.join(locked) + '\n\nCommand not runned.', exit_status)
        
def check_required(actions):
    not_done= done_file.not_done(actions)
    if not_done:
        exit_status= int(not required_permissive)
        exit('The following actions are required but not marked as done:\n ' + ' '.join(not_done) +'\n\n Command not runned.', exit_status)



def handle_exec(cmd, required_actions, produced_actions, to_lock_actions):

    check_required(required_actions)
    check_produced(produced_actions)
    sys_ret= os.WEXITSTATUS(os.system(cmd))
    manage_command_ret(sys_ret)
    done_file.set_done(produced_actions)
    done_file.lock(to_lock_actions)
    done_file.save()


def handle_init(path):
    Done_file.init_done_dir(path)

args=parser.getArgs()

path= args['done_dir_path']
mode= args['mode']
if mode == 'init':
    handle_init(path)

elif mode == 'exec':
    cmd=args['command']
    lock_no_fail= args['lock_no_fail']
    required_permissive= args['required_permissive']
    child_permissive=args['child_permissive']

    required= args['required_action']
    produced= args['produced_action']
    lock= args['lock_action']
    lock_products=args['lock_products']
    done_file= Done_file(path)
    if lock_products:
        lock.extend(produced)

    handle_exec(cmd, required, produced, lock)











