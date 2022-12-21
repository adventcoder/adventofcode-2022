import framework
from operator import add, sub, mul

def safediv(x, y):
    assert x % y == 0
    return x // y

def flip(op):
    return lambda x, y: op(y, x)

ops = { '+': add, '-': sub, '*': mul, '/': safediv }
left_inverse = { '+': sub, '-': add, '*': safediv, '/': mul }
right_inverse = { '+': sub, '-': flip(sub), '*': safediv, '/': flip(safediv) }

def solve(input):
    jobs = parse_jobs(input)
    yield speak('root', jobs)
    yield reverse_speak('humn', jobs, reverse(jobs))

def parse_jobs(input):
    jobs = {}
    for line in input.splitlines():
        key, value = line.split(':')
        tokens = value.split()
        jobs[key.strip()] = int(tokens[0]) if len(tokens) == 1 else tokens
    return jobs

def speak(name, jobs):
    job = jobs[name]
    if isinstance(job, int):
        return job
    else:
        left, opname, right = job
        return ops[opname](speak(left, jobs), speak(right, jobs))

def reverse_speak(name, jobs, parents):
    parent = parents[name]
    left, opname, right = jobs[parent]
    if parent == 'root':
        if name == left:
            return speak(right, jobs)
        elif name == right:
            return speak(left, jobs)
    else:
        if name == left:
            return left_inverse[opname](reverse_speak(parent, jobs, parents), speak(right, jobs))
        elif name == right:
            return right_inverse[opname](reverse_speak(parent, jobs, parents), speak(left, jobs))

def reverse(jobs):
    parents = {}
    for name, job in jobs.items():
        if not isinstance(job, int):
            left, _, right = job
            parents[left] = name
            parents[right] = name
    return parents

if __name__ == '__main__':
    framework.main()
