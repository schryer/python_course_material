
# coding: utf-8

# ## Fundamental Python types
# 
# Python has a number of fundamental types.  Please explore the code below to see what they are.

# In[ ]:

a = 1; b = 10000000000000000000000000
type(a), type(b)


# In[ ]:

c = 1.0
type(c)


# ### The boolean type can contain the values `True` and `False` which always start with capital letters:

# In[ ]:

d1 = True
d2 = False

type(d1)


# ### Complex numbers are a fundamental type: note the use of `j` to specify the imaginary part

# In[ ]:

e = 1.0 - 1.0j
type(e)


# ### The `None` type 
# 
# This type is very commonly used and also starts with a capital `N`.    

# In[ ]:

f = None


# ## All types have properties 
# 
# The variable `c` defined above is an integer type.  This type has the following properties that are accessed with dot notation.  The dot can be thought of as meaning "get something from the thing on the left" (in this case `c`).
#  
#     c.bit_length    c.conjugate    c.denominator    c.imag    c.numerator    c.real
#     
# In this case `c.bit_length` is actually a function which must be *called* using round brackets `()`to use (more on functions later).

# In[ ]:

a.real, a.bit_length()


# ## Some properties are hidden
# 
# Although `f` is a `None` type, it still has hidden properties.

# In[ ]:

f.__sizeof__()


# ## Many types have common properties 
# 
# Python has been designed such that its types are as compatible as possible with each other.
# This is done by giving them common properties so that the same Python code is able to process different types.
# 
# ## Exercise:  Find the common properties between the types listed above

print ("Hello Universe!")
