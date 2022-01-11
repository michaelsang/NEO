import operator
import itertools

class UnsupportedCriterionError(NotImplementedError):
    """
    A class to represent an UnsupportedCriterionError object.

    ...

    Attributes
    ----------
    None

    Methods
    -------
    None

    """


class AttributeFilter:
    """
    A general superclass to represent an AttributeFilter object.

    ...

    Attributes
    ----------
    op
    value

    Methods
    -------
    get

    """

    def __init__(self, op, value):
        """
        Constructs all the necessary attributes for the AttributeFilter.

        Parameters
        ----------
        op: str
            A 2-argument predicate comparator.
        value: int
            The reference value to compare against.
        """
        self.op = op
        self.value = value

    def __call__(self, approach):
        """
        Invoke self(approach).

        Parameters
        ----------
        approach: str

        Return
        ------
        Invoke self.approach
        """
        return self.op(self.get(approach), self.value)

    @classmethod
    def get(cls, approach):
        """
        Get an attribute of interest from a close approach.

        Parameters
        ----------
        cls: self
        approach: str
            A CloseApproach on which to evaluate this filter.

        Return
        ------
        The value of an attribute of interest.
        """
        raise UnsupportedCriterionError

    def __repr__(self):
        """
        Returns a printable representation of the object.
        """
        return f"{self.__class__.__name__}(op=operator.{self.op.__name__},"
        "value={self.value})"


class DateFilter(AttributeFilter):
    """
    A class DateFilter that inherits from AttributeFilter superclass.

    Methods
    -------
    get(cls, approach)
    """
    @classmethod
    def get(cls, approach):
        """
        Get date time of interest of close approach.

        Parameters
        ----------
        cls: self
        approach: str

        Returns
        -------
        Approach's date time
        """
        return approach.time.date()


class DistanceFilter(AttributeFilter):
    """
    A class DistanceFilter that inherits from AttributeFilter superclass.

    Methods
    -------
    get(cls, approach)
    """
    @classmethod
    def get(cls, approach):
        """
        Get distance of interest from close approach.

        Parameters
        ----------
        cls: self
        approach: str

        Returns
        -------
        Approach's distance
        """
        return approach.distance


class VelocityFilter(AttributeFilter):
    """
    A class VelocityFilter that inherits from AttributeFilter superclass.

    Methods
    -------
    get(cls, approach)
    """
    @classmethod
    def get(cls, approach):
        """
        Get an velocity of interest from close approach.

        Parameters
        ----------
        cls: self
        approach: str

        Returns
        -------
        Approach's velocity
        """
        return approach.velocity


class DiameterFilter(AttributeFilter):
    """
    A class DiameterFilter that inherits from AttributeFilter superclass.

    Methods
    -------
    get(cls, approach)
    """
    @classmethod
    def get(cls, approach):
        """
        Get an diameter of interest from neo.

        Parameters
        ----------
        cls: self
        approach: str

        Returns
        -------
        Approach's diameter
        """
        return approach.neo.diameter


class HazardousFilter(AttributeFilter):
    """
    A class HazardousFilter that inherits from AttributeFilter superclass.

    Methods
    -------
    get(cls, approach)
    """
    @classmethod
    def get(cls, approach):
        """
        Get hazardous of interest from neo.

        Parameters
        ----------
        cls: self
        approach: str

        Returns
        -------
        Approach's hazardous
        """
        return approach.neo.hazardous


def create_filters(
        date=None, start_date=None, end_date=None,
        distance_min=None, distance_max=None,
        velocity_min=None, velocity_max=None,
        diameter_min=None, diameter_max=None,
        hazardous=None
):
    """Create a collection of filters from user-specified criteria.
    Each of these arguments is provided by the main module with a value from the
    user's options at the command line. Each one corresponds to a different type
    of filter. For example, the `--date` option corresponds to the `date`
    argument, and represents a filter that selects close approaches that occurred
    on exactly that given date. Similarly, the `--min-distance` option
    corresponds to the `distance_min` argument, and represents a filter that
    selects close approaches whose nominal approach distance is at least that
    far away from Earth. Each option is `None` if not specified at the command
    line (in particular, this means that the `--not-hazardous` flag results in
    `hazardous=False`, not to be confused with `hazardous=None`).
    The return value must be compatible with the `query` method of `NEODatabase`
    because the main module directly passes this result to that method. For now,
    this can be thought of as a collection of `AttributeFilter`s.
    :param date: A `date` on which a matching `CloseApproach` occurs.
    :param start_date: A `date` on or after which a matching `CloseApproach` occurs.
    :param end_date: A `date` on or before which a matching `CloseApproach` occurs.
    :param distance_min: A minimum nominal approach distance for a matching `CloseApproach`.
    :param distance_max: A maximum nominal approach distance for a matching `CloseApproach`.
    :param velocity_min: A minimum relative approach velocity for a matching `CloseApproach`.
    :param velocity_max: A maximum relative approach velocity for a matching `CloseApproach`.
    :param diameter_min: A minimum diameter of the NEO of a matching `CloseApproach`.
    :param diameter_max: A maximum diameter of the NEO of a matching `CloseApproach`.
    :param hazardous: Whether the NEO of a matching `CloseApproach` is potentially hazardous.
    :return: A collection of filters for use with `query`.
    """
    # TODO: Decide how you will represent your filters.
    # return a collection of filters as list
    filters = []
    if date is not None:
        filters.append(DateFilter(operator.eq, date))
    if start_date is not None:
        filters.append(DateFilter(operator.ge, start_date))
    if end_date is not None:
        filters.append(DateFilter(operator.le, end_date))
    if distance_min is not None:
        filters.append(DistanceFilter(operator.ge, distance_min))
    if distance_max is not None:
        filters.append(DistanceFilter(operator.le, distance_max))
    if velocity_min is not None:
        filters.append(VelocityFilter(operator.ge, velocity_min))
    if velocity_max is not None:
        filters.append(VelocityFilter(operator.le, velocity_max))
    if diameter_min is not None:
        filters.append(DiameterFilter(operator.ge, diameter_min))
    if diameter_max is not None:
        filters.append(DiameterFilter(operator.le, diameter_max))
    if hazardous is not None:
        filters.append(HazardousFilter(operator.eq, hazardous))
    return tuple(filters)

def limit(iterator, n=None):
    """
    Produce a limited stream of values from an iterator.

            Parameters:

                iterator (int): An iterator of values.
                n (None): The maximum number of values to produce.
                yield : The first (at most) n values from the iterator.

            Returns:

                None
    """
 #   for i, v in enumerate(iterator):
 #       yield v
 #       if i + 1 == n:
 #           break

    if n == 0 or n == None:
        return iterator
    return itertools.islice(iterator, n)