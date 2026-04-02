---
title: Data-Driven Design
layout: default
---

{% assign visible_tutorials = site.tutorials | where_exp: "item", "item.slug != 'home'" | sort: "title" %}
{% assign gis_tutorials = visible_tutorials | where_exp: "item", "item.category == 'gis'" %}
{% assign data_tutorials = visible_tutorials | where_exp: "item", "item.category == 'data-science'" %}
{% assign nlp_tutorials = visible_tutorials | where_exp: "item", "item.category == 'nlp'" %}

<section class="home-hero">
  <p class="eyebrow">Public tutorial library</p>
  <h1 class="home-title">Data-driven methods for design students who need more than intuition.</h1>
  <p class="home-intro">This collection teaches GIS, remote sensing, data visualization, and NLP as working design tools: ways to read territory, measure change, build evidence, and communicate research with clarity.</p>
  <p class="home-note">{{ visible_tutorials | size }} tutorials across GIS, data science, and NLP, written for architecture, landscape, urban, and research practice.</p>
</section>

<section class="home-section" id="gis">
  <div class="section-head">
    <p class="eyebrow">01</p>
    <div>
      <h2>GIS and Remote Sensing</h2>
      <p>Terrain, imagery, climate, land cover, solar exposure, and spatial analysis for environmental and urban questions.</p>
    </div>
  </div>

  <div class="tutorial-list">
    {% for tutorial in gis_tutorials %}
    <a class="tutorial-row" href="{{ tutorial.url | relative_url }}">
      <div class="tutorial-row-main">
        <h3>{{ tutorial.title }}</h3>
        {% if tutorial.subtitle %}
        <p>{{ tutorial.subtitle }}</p>
        {% endif %}
      </div>
      <div class="tutorial-row-meta">
        <p>{{ tutorial.difficulty | default: 'tutorial' }}</p>
        {% if tutorial.tools and tutorial.tools.size > 0 %}
        <p>{{ tutorial.tools | slice: 0, 3 | join: ' / ' }}</p>
        {% endif %}
      </div>
    </a>
    {% endfor %}
  </div>
</section>

<section class="home-section" id="data-science">
  <div class="section-head">
    <p class="eyebrow">02</p>
    <div>
      <h2>Data Visualization and Data Science</h2>
      <p>Collection, cleanup, plotting, and interpretation workflows that turn raw information into readable arguments.</p>
    </div>
  </div>

  <div class="tutorial-list">
    {% for tutorial in data_tutorials %}
    <a class="tutorial-row" href="{{ tutorial.url | relative_url }}">
      <div class="tutorial-row-main">
        <h3>{{ tutorial.title }}</h3>
        {% if tutorial.subtitle %}
        <p>{{ tutorial.subtitle }}</p>
        {% endif %}
      </div>
      <div class="tutorial-row-meta">
        <p>{{ tutorial.difficulty | default: 'tutorial' }}</p>
        {% if tutorial.tools and tutorial.tools.size > 0 %}
        <p>{{ tutorial.tools | slice: 0, 3 | join: ' / ' }}</p>
        {% endif %}
      </div>
    </a>
    {% endfor %}
  </div>
</section>

<section class="home-section" id="nlp">
  <div class="section-head">
    <p class="eyebrow">03</p>
    <div>
      <h2>Natural Language Processing</h2>
      <p>Text cleaning, exploratory analysis, and computational reading methods for research that works with language as data.</p>
    </div>
  </div>

  <div class="tutorial-list">
    {% for tutorial in nlp_tutorials %}
    <a class="tutorial-row" href="{{ tutorial.url | relative_url }}">
      <div class="tutorial-row-main">
        <h3>{{ tutorial.title }}</h3>
        {% if tutorial.subtitle %}
        <p>{{ tutorial.subtitle }}</p>
        {% endif %}
      </div>
      <div class="tutorial-row-meta">
        <p>{{ tutorial.difficulty | default: 'tutorial' }}</p>
        {% if tutorial.tools and tutorial.tools.size > 0 %}
        <p>{{ tutorial.tools | slice: 0, 3 | join: ' / ' }}</p>
        {% endif %}
      </div>
    </a>
    {% endfor %}
  </div>
</section>

<section class="home-closing">
  <p class="eyebrow">Method</p>
  <p>These tutorials are written for readers who need practical technical instruction, but also need to understand what data reveals, what it hides, and how design decisions change when evidence becomes legible.</p>
</section>
