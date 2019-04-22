def job(prev_state={'job_ident': None, 'log': ''}, action=None):
    state = prev_state

    if action == None:
        pass

    elif action.type == 'START_JOB':
        state['job_ident'] = action.payload['ident']
        state['log'] = ''

    elif action.type == 'FINISH_JOB':
        state['job_ident'] = None

    elif action.type == 'ADD_LOG':
        state['log'] += action.payload['text']

    return state
