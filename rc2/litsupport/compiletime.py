import lit.Test
from litsupport import timeit
import os


def _getCompileTime(context):
    # We compile multiple benchmarks in the same directory in SingleSource
    # mode. Only look at compiletime files starting with the name of our test.
    prefix = ""
    if context.config.single_source:
        prefix = "%s." % os.path.basename(context.executable)

    compile_time = 0.0
    link_time = 0.0
    dir = os.path.dirname(context.test.getFilePath())
    for path, subdirs, files in os.walk(dir):
        for file in files:
            if file.endswith('.o.time') and file.startswith(prefix):
                fullpath = os.path.join(path, file)
                compile_time += timeit.getUserTime(fullpath)
            if file.endswith('.link.time') and file.startswith(prefix):
                fullpath = os.path.join(path, file)
                link_time += timeit.getUserTime(fullpath)
    return {
        'compile_time': lit.Test.toMetricValue(compile_time),
        'link_time': lit.Test.toMetricValue(link_time),
    }


def mutatePlan(context, plan):
    plan.metric_collectors.append(_getCompileTime)
