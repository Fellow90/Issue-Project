GENDER_CHOICES = (
    ('M','Male'),
    ('F','Female'),
    ('O','Others'),
)


STATUS_CHOICES = (
    ('100', 'PENDING'),
    ('200', 'RESOLVED'),
    ('102', 'FORWARDED'),
)

ROLE_CHOICES = (
    ('Normal User','Normal User'),
    ('L1 User','L1 User'),
    ('L2 User','L2 User'),
    ('L3 User','L3 User'),
    ('Admin','Admin'),
)

PRIORITY_CHOICES = (
    ('High', 'High'),
    ('Medium', 'Medium'),
    ('Low', 'Low'),
)
GROUP_CHOICES = (
    ('L1','L1'),
    ('L2','L2'),
    ('L3','L3'),
)
RESOLVED_BY_CHOICES = (
    ('L1','L1'),
    ('L2','L2'),
    ('L3','L3'),
)