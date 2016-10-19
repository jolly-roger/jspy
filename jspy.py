#!/usr/bin/env python

import os
import sys
import traceback

from js.exception import JsException
from js.interpreter import Interpreter, load_file


def main(argv):
    opts, files = parse_args(argv)

    try:
        run(files, opts)
    except:
        traceback.print_exc()

    return 0


def run(files, opts):
    interactive = len(files) == 0
    inspect = opts.get('inspect', False)
    interp = Interpreter(opts)

    for filename in files:
        src = load_file(filename)

        try:
            interp.run_src(src)
        except JsException as e:
            printerrormessage(unicode(filename), e._msg())
        except Exception as e:
            printerror(unicode(filename), e, src)

    if inspect or interactive:
        repl(interp)


def printerrormessage(filename, message):
    print(u"ERROR in %s: %s\n" % (filename, message))


def repl(interpreter):
    filename = u'<stdin>'
    while True:
        print(u'js> ')
        line = readline()

        try:
            result = interpreter.run_src(line)
            result_string = result.to_string()
            print(u"%s\n" % (result_string))
        except JsException as e:
            printerrormessage(unicode(filename), e._msg())
            continue
        except Exception as e:
            if hasattr(e, 'source_pos'):
                printerror(unicode(filename), e, line)
            else:
                traceback.print_exc()
            continue


def print_sourcepos(filename, source_pos, source):
    marker_indent = u' ' * source_pos.columnno
    error_lineno = source_pos.lineno - 1
    error_line = (source.splitlines())[error_lineno]
    print(u'Syntax Error in: %s:%d\n' % (unicode(filename), error_lineno))
    print(u'%s\n' % (unicode(error_line)))
    print(u'%s^\n' % (marker_indent))


def printerror(filename, exc, source):
    print_sourcepos(filename, exc.source_pos, source)
    error = exc.errorinformation.failure_reasons
    print(u'Error: %s\n' % (unicode(str(error))))

def readline():
    result = []
    while True:
        s = os.read(0, 1)
        result.append(s)
        if s == "\n":
            break
        if s == '':
            if len(result) > 1:
                break
            raise Exception
    return "".join(result)


def _parse_bool_arg(arg_name, argv):
    for i in xrange(len(argv)):
        if argv[i] == arg_name:
            del(argv[i])
            return True
    return False


def parse_args(argv):
    opts = {}

    opts['debug'] = _parse_bool_arg('-d', argv) or _parse_bool_arg('--debug', argv)
    opts['inspect'] = _parse_bool_arg('-i', argv) or _parse_bool_arg('--inspect', argv)

    del(argv[0])

    return opts, argv


if __name__ == '__main__':
    main(sys.argv)


# _____ Define and setup target ___
def target(driver, args):
    driver.exe_name = 'py-js'
    return entry_point, None


def entry_point(argv):
    return main(argv)
