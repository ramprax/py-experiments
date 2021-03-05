"""
Trying to mimic a bit of the javascript promise api minus the async part
"""


class Rejected(Exception):
    pass


class UnhandledRejection(Exception):
    pass


class JSPromise:
    STATE_PENDING = 'pending'
    STATE_FULFILLED = 'fulfilled'
    STATE_REJECTED = 'rejected'

    def __str__(self):
        return f'{self.__class__.__name__}:<state={self._state},return-value={self._ret_val},reject-reason={self._rej_reason},rejection-handled={self._rej_handled}>'

    def __init__(self, executorFunc):
        self._executor = executorFunc
        self._state = self.STATE_PENDING
        self._ret_val = None
        self._rej_reason = None
        self._rej_handled = None

    def _execute(self):
        if self._state == self.STATE_PENDING:
            try:
                ret_val = self._executor(self._set_fulfilled, self._set_rejected)

                if self._state == self.STATE_PENDING:
                    # In case the executor func simply returned a value without calling resolve()
                    self._set_fulfilled(ret_val)

            except Exception as ex:
                self._set_rejected(ex)

    def _set_fulfilled(self, val):
        if self._state != self.STATE_PENDING:
            raise Exception('Already settled')

        self._state = self.STATE_FULFILLED
        self._ret_val = val

    def _set_rejected(self, reason):
        if self._state != self.STATE_PENDING:
            raise Exception('Already settled')

        self._state = self.STATE_REJECTED
        if isinstance(reason, Rejected):
            self._rej_reason = reason
        elif reason is not None:
            self._rej_reason = Rejected(reason)
        else:
            self._rej_reason = Rejected()

        if self._rej_handled is None:
            self._rej_handled = False

    def __del__(self):
        print('In __del__(): before _execute(): ', str(self))
        self._execute()
        print('In __del__(): after _execute(): ', str(self))
        if self._state == self.STATE_REJECTED and not self._rej_handled:
            raise UnhandledRejection(self._rej_reason) from self._rej_reason

    def then(self, resolveFunc, rejectFunc=None):
        self._execute()

        nextVal = rejVal = None
        if self._state == self.STATE_FULFILLED:
            nextVal = resolveFunc(self._ret_val)
            return self.resolve(nextVal)
        elif self._state == self.STATE_REJECTED:
            if rejectFunc:
                try:
                    self._rej_handled = True
                    nextRejVal = rejectFunc(self._rej_reason)

                    if isinstance(nextRejVal, JSPromise):
                        rejPromise = nextRejVal
                    else:
                        rejPromise = self.reject(nextRejVal)
                        rejPromise._rej_handled = True

                    return rejPromise
                except Exception as ex:
                    return self.reject(ex)
            else:
                return self

        raise Exception('Should not reach here')

    def catch(self, catcher):
        self._execute()
        if self._state == self.STATE_REJECTED and not self._rej_handled:
            self._rej_handled = True
            catcher(self._rej_reason)
        return self

    def Finally(self, ff):
        print('In Finally(): before _execute(): ', str(self))
        self._execute()
        print('In Finally(): after _execute(): ', str(self))
        try:
            ff()
        except Exception as ex:
            print('Ignoring exception in finally(): ', ex)

        return self

    @classmethod
    def resolve(cls, value):
        if isinstance(value, cls):
            return value

        def my_ex(res, rej=None):
            return res(value)

        return cls(my_ex)

    @classmethod
    def reject(cls, reason):
        if isinstance(reason, cls):
            return reason

        def my_ex(res, rej):
            return rej(reason)

        return cls(my_ex)

