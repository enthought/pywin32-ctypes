{{ name }}
{{ underline }}

.. automodule:: {{ fullname }}
   {% block functions %}
   {% if functions %}
   .. rubric:: Functions

   .. autosummary::
   {% for item in functions %}
      {{ item }}
   {%- endfor %}

   |
   |

   {% for item in functions %}
   .. autofunction:: {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}
   {% block classes %}
   {% if classes %}
   .. rubric:: Classes

   .. autosummary::

   {% for item in classes %}
      {{ item }}
   {%- endfor %}

   |
   |

   {% for item in classes %}
   {% if item.__module__ == module %}
   .. autoclass:: {{ item }}
   {%- endif %}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block exceptions %}
   {% if exceptions %}
   .. rubric:: Exceptions

   .. autosummary::

   {% for item in exceptions %}
      {{ item }}
   {%- endfor %}

   |
   |

   {% for item in exceptions %}
   .. autoclass:: {{ item }}

   {%- endfor %}
   {% endif %}
   {% endblock %}
