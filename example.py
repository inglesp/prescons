print "hello world"
def fn(x):
    if x > 0:
        print x
    else:
        raise Exception

fn(1)
fn(-1)
