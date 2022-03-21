import threading
import win32serviceutil
from win10toast_click import ToastNotifier
import datetime
toaster = ToastNotifier()


def main():
    '''Define detection module'''
    #  0: "UNKNOWN"
    #  1: "STOPPED"
    #  2: "START_PENDING"
    #  3: "STOP_PENDING"
    #  4: "RUNNING"
    def is_iterable(source):
        if source is not None:
            try:
                iter(source)
            except TypeError:
                return False
            return True
        else:
            raise RuntimeError("argument cannot be None")

    def status_service(service_name):
        try:
            result = win32serviceutil.QueryServiceStatus(service_name)[1]
            if result == 4:  # running!
                return True
            elif result == 1:  # braked!
                return False
            else:
                return result
        except Exception as e:
            if e.args:
                args = list()
                for arg in e.args:
                    if is_iterable(arg):
                        args.append(str(eval(repr(arg)), 'gbk'))
                    else:
                        args.append(arg)
                raise RuntimeError("Error:", args[-1], tuple(args))
            else:
                raise RuntimeError(
                    "Uncaught exception, maybe it is a 'Access Denied'")

    def stop_service(service_name):
        status = status_service(service_name)
        if status == True:
            try:
                win32serviceutil.StopService(service_name)
            except Exception as e:
                if e.args:
                    # print e.args
                    args = list()
                    for arg in e.args:
                        if is_iterable(arg):
                            args.append(str(eval(repr(arg)), 'gbk'))
                        else:
                            args.append(arg)
                    print("Error:", args[-1], tuple(args))
                    raise RuntimeError
                else:
                    raise RuntimeError(
                        "Uncaught exception, maybe it is a 'Access Denied'")

    '''write log'''
    def writelog():
        log = open('log.txt', 'a')
        time = datetime.datetime.now()
        log.writelines("[" + str(time) + "] " +
                       "Camera detected being used." + "\n")
        log.close()

    while True:
        '''read log'''
        log = open("log.txt", "r+")
        line = log.read().splitlines()
        list1 = line[1:2]
        logger = ''.join(list1)
        log.close()
        if status_service("FrameServer") == True:
            toaster.show_toast("E-B:Camera detected being used!",
                               "If you aren't using it, open Emergency-Brakes and click 'Brake'.",
                               icon_path="image/warning.ico",
                               threaded=False)
            if logger == "True":
                writelog()


if __name__ == "__main__":
    main()