from json import dumps
import ramda as R


class FilterError(Exception):
    pass


class Matcher:

    @classmethod
    def traverse(cls, subject, callback, left=None, sign=1, lazy=False, argT=lambda *args: args):

        if callable(callback):
            return callback(*argT(subject, sign))

        if isinstance(callback, (list, tuple)):

            if callback[0] == '&':
                #if not isinstance(left, bool):
                #    raise FilterError('and must be preceeded with condition.')

                if lazy:
                    return left and cls.traverse(subject, callback[1:], sign=sign, lazy=lazy, argT=argT)
                return cls.traverse(subject, callback[1:], sign=sign, lazy=lazy, argT=argT) and left

            if callback[0] == '|':
                #if not isinstance(left, bool):
                #    raise FilterError('or must be preceeded with condition.')

                if lazy:
                    return left or cls.traverse(subject, callback[1:], sign=sign, lazy=lazy, argT=argT)
                return cls.traverse(subject, callback[1:], sign=sign, lazy=lazy, argT=argT) or left

            if callback[0] == '!':
                return not cls.traverse(subject, callback[1:], left=left, sign=-sign, lazy=lazy, argT=argT)

            if len(callback) == 1:
                return cls.traverse(subject, callback[0], left=left, sign=sign, lazy=lazy, argT=argT)

            return cls.traverse(subject, callback[1:],
                                left=cls.traverse(subject, callback[0], left=left, sign=sign, lazy=lazy, argT=argT),
                                sign=sign, lazy=lazy, argT=argT)

        raise FilterError('Unknown condition: {}'.format(dumps(callback)))

    @classmethod
    def isMatch(cls, subject, test):

        return cls.traverse(subject, test, lazy=True, argT=lambda subject, *args: (subject,))

    @classmethod
    def match(cls, subjects, test, left=None):
        return R.filter(lambda subject: cls.isMatch(subject, test))(subjects)
