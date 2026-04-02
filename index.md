---
title: Data-Driven Design
layout: default
---

Welcome to the public tutorial library for GIS, data science, data visualization, and NLP workflows for design students.

{% assign visible_tutorials = site.tutorials | where_exp: "item", "item.slug != 'home'" | sort: "title" %}

## GIS

{% for tutorial in visible_tutorials %}
{% assign tutorial_category = tutorial.category | downcase %}
{% if tutorial_category == "gis" %}
- [{{ tutorial.title }}]({{ tutorial.url | relative_url }})
{% endif %}
{% endfor %}

## Data Science

{% for tutorial in visible_tutorials %}
{% assign tutorial_category = tutorial.category | downcase %}
{% if tutorial_category == "data-science" %}
- [{{ tutorial.title }}]({{ tutorial.url | relative_url }})
{% endif %}
{% endfor %}

## NLP

{% for tutorial in visible_tutorials %}
{% assign tutorial_category = tutorial.category | downcase %}
{% if tutorial_category == "nlp" %}
- [{{ tutorial.title }}]({{ tutorial.url | relative_url }})
{% endif %}
{% endfor %}

## Notes

- This site is built from the `_tutorials/` collection.
- Working files and source archives are intentionally excluded from the public publish.
