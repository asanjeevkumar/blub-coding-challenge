Create dev env for bulb energy usage
====================================

Build venv:

    make venv

Activate venv:

    source venv/bin/activate
    
Run the command:

    python main.py 
    
    or
    
    python main.py --member_id=mem_id --account_id=acc_id --bill_date="yyyy-mm-dd"
    
Other useful commands:
    
    make check
    make check-tests
    make check-coding-standards
    
For cleaning up:
    
    make clean
