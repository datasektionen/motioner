{% if document_type == 'motion'  %}
#Motion angående {{ title }}
{% elif document_type == 'proposition'  %}
#Proposition angående {{ title }}
{% elif document_type == 'reply' %}
#Svar på motion angående {{ title }}
{% elif document_type == 'change' %}
#Ändringsyrkande för motion angående {{ title }}
{% else  %}
#{{ title }}
{% endif  %}

##Bakgrund
{{ background }}

##Förslag till beslut

{% if document_type == 'motion'  %}
	Mot bakgrund av ovanstående yrkar {{ i_or_we }}:
{% endif %}

{% for item in items  %}
- _att_ {{ item }}
{% endfor %}

{% if document_type != 'motion'  %}
D-rektoratet, genom
{% endif %}

{% for author in authors  %}
- {{ author }}
{% endfor %}

Skickat av {{ first_name }} {{ last_name }} {{ emails }}
