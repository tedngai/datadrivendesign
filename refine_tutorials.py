#!/usr/bin/env python3
import os

TUTORIALS = {
    "/home/tngai/data/Tutorials/_tutorials/digital-topography.md": """## Introduction

Digital topography is the study of Earth's surface shape and elevation—mountains, valleys, rivers, ridges—expressed as data that computers can read and designers can manipulate. Where a traditional site plan shows contours as thin lines on paper, digital elevation models (DEMs) treat elevation as a continuous data field: every point on a site has an exact height value. This allows you to query slopes, calculate viewsheds, generate 3D meshes, and integrate real terrain into your design software. For architects, landscape architects, and urban designers, digital topography transforms site analysis from intuition into evidence.

DEMs come in two main flavors. Digital Elevation Models (DEMs) represent bare ground terrain, while Digital Surface Models (DSMs) include everything on top of the terrain—buildings, trees, bridges. Most open-access elevation data, like the USGS 3DEP program providing 1-meter resolution across the United States, is DSM data captured from airborne LiDAR. Understanding this distinction matters: if you're analyzing solar access, you'll want a DSM that includes building heights; if you're modeling water flow, you want a DEM with structures removed so water moves across actual ground.

The practical power of digital topography lies in scale. You can now download high-resolution elevation data for any location in the US for free—data that previously required expensive aerial surveys. This democratization means student designers can incorporate real site conditions into early concept sketches, test grading schemes in 3D, or visualize how a building sits in relation to surrounding terrain without conducting expensive site visits.

## Historical Context

The measurement and representation of terrain has ancient roots—contour lines appeared on maps by the 1700s, and by the 19th century, military cartographers had developed systematic surveying methods. The real transformation came with remote sensing: radar and LiDAR (Light Detection and Ranging) from aircraft, and later satellites, allowed systematic measurement of elevation across vast areas without physical survey crews.

The USGS began systematic elevation mapping in the 1930s using photogrammetry (measuring from overlapping aerial photographs), but coverage was incomplete and resolution limited. The 2000s saw a major leap with shuttle-based radar missions like SRTM (Shuttle Radar Topography Mission), which captured near-global elevation at 30-meter resolution. Today, the USGS 3DEP program, launched in 2015, aims for nationwide LiDAR coverage at 1-meter resolution—delivering data that was unthinkable at mass scale just two decades ago.

Software evolved alongside data. Early GIS tools like GRASS (developed by the US Army Corps of Engineers in the 1980s) could process elevation grids, but workflows were arcane. Modern tools like QGIS have democratized these capabilities, putting professional-grade terrain analysis within reach of anyone with a laptop and internet connection.

## Design Relevance

Digital topography fundamentally changes how designers interact with site. Traditional site analysis happens in stages: site visit, paper drawings, mental modeling, then eventually a 3D representation. Digital elevation data collapses this pipeline—you can sketch on top of real terrain from day one, testing massing positions against actual slopes, views, and drainage patterns.

For landscape architecture and urban design, terrain is destiny. Slope determines what can be built, where water flows, how people move through space. A site that appears flat in a site visit might reveal subtle grade changes that dramatically affect drainage or accessibility. Digital topography surfaces these conditions before you're on site, enabling smarter preliminary design decisions.

The ability to generate 3D meshes from elevation data means terrain becomes a design medium itself. Rhino and 3DS Max workflows allow you to sculpt digital terrain, test cut-and-fill scenarios, or visualize proposed grading in context with existing conditions. This is especially valuable for stormwater management designs—understanding how water moves across terrain helps create sustainable drainage systems that work with natural patterns rather than against them.

## Resources & Further Reading

- [USGS 3DEP Elevation Data](https://www.usgs.gov/3d-elevation-program) - Free access to LiDAR-derived elevation data across the US at varying resolutions
- [USGS National Map Download](https://apps.nationalmap.gov/downloader/#/) - Direct portal for downloading elevation, imagery, and other geospatial data
- [NOAA Coastal Elevation Models](https://www.ngdc.noaa.gov/mgg/coastal/coastal.html) - Bathymetric and coastal elevation data for sea level rise and flood analysis
- [QGIS Documentation: DEM Terrain Analysis](https://docs.qgis.org/latest/en/docs/user_manual/working_with_raster/raster_analysis.html) - Official guide to terrain analysis tools in QGIS
- [USGS LiDAR 101](https://www.usgs.gov/faqs/what-lidar) - Plain-language introduction to LiDAR technology and data formats
""",
    "/home/tngai/data/Tutorials/_tutorials/lidar-processing.md": """## Introduction

LiDAR—Light Detection and Ranging—is a remote sensing technology that fires rapid pulses of laser light at a surface and measures how long it takes for each pulse to bounce back. By calculating the travel time and angle of thousands or millions of returns, LiDAR builds a precise, 3D point cloud representation of the terrain and everything on it: buildings, trees, power lines, bridges. The result is essentially a digital twin of the physical world at the moment the data was captured.

What makes LiDAR special for design is its combination of precision and coverage. Traditional surveying captures discrete points—elevation at specific locations. LiDAR captures millions of points continuously, creating a dataset dense enough to capture building edges, tree canopy shapes, and subtle terrain variations simultaneously. For site analysis, this means you can extract building footprints, model terrain, analyze viewsheds, and assess vegetation—all from a single dataset.

Modern open-access LiDAR data, largely available through USGS programs and state initiatives, has transformed what's possible in design education and practice. Where once only large infrastructure projects could afford LiDAR surveys, designers can now download pre-captured data covering most of the United States at resolutions ranging from 30 meters to as fine as 0.5 meters for some urban areas.

## Historical Context

LiDAR's origins trace to the 1960s, shortly after the invention of the laser. Early applications were primarily atmospheric research—measuring cloud heights, atmospheric particles, and cloud structure. The technology advanced through the 1970s and 1980s as GPS and inertial measurement units improved, allowing accurate geo-referencing of point clouds from aircraft.

The 1990s saw LiDAR migrate to civilian applications, particularly mapping and elevation modeling. NASA's SRTM mission in 2000 demonstrated space-based LiDAR's potential for global elevation mapping. Around the same time, full-waveform LiDAR emerged, capturing the entire return signal rather than just discrete points, enabling better discrimination of ground returns from vegetation.

The 2010s brought a revolution in data availability. The USGS 3DEP program, initiated in 2015, committed to making high-quality elevation data freely available across the United States. State governments, especially those coastal states concerned about flooding, invested heavily in LiDAR acquisition. Today, over 50% of the US has LiDAR coverage at 1-meter resolution or better, with coverage expanding annually.

Simultaneously, processing software evolved from specialized, expensive packages to accessible tools. Cloud Compare, developed as an open-source PhD project, now handles millions of points on a standard laptop. This democratization means design students can work with the same caliber of data that previously required specialized GIS departments.

## Design Relevance

For designers, LiDAR is primarily valuable as a source of Digital Surface Models (DSMs) and Digital Elevation Models (DEMs). The distinction matters: a DSM includes everything the laser hit—rooftops, tree canopies, vehicles—while a DEM represents bare earth with structures removed. Your choice depends on the design question: solar analysis needs DSM data (buildings block and cast shadows), while drainage modeling needs DEM (water flows across ground, not rooftops).

The point cloud itself contains rich information beyond simple elevation. LiDAR intensity data indicates surface reflectivity—hard surfaces like asphalt reflect differently than vegetation or buildings. Classified point clouds separate ground points from vegetation, buildings, and noise, enabling specialized analyses like building footprint extraction or tree height estimation.

Viewshed analysis—the ability to see what is visible from a given point—is one of LiDAR's most design-relevant applications. Combined with building height data, designers can assess how proposed massing affects sightlines, solar access, or visual impact on surrounding areas. This type of analysis previously required expensive consultant studies; now it's accessible in QGIS with publicly available data.

LiDAR data also enables accurate 3D modeling workflows. Point clouds can be meshed to create triangulated surfaces, which can then be simplified and optimized for visualization or further design work. This bridges the gap between field-captured reality and design software like Rhino or Revit.

## Resources & Further Reading

- [Cloud Compare Open Source](https://www.danielgm.net/cc/) - Free, powerful point cloud processing software with excellent tutorials
- [USGS LiDAR Documentation](https://www.usgs.gov/3d-elevation-program/lidar) - Comprehensive guide to LiDAR data types, formats, and access
- [NOAA Digital Coast LiDAR](https://coast.noaa.gov/dataviewer/#/) - Coastal-focused LiDAR data portal with high-resolution coverage
- [State LiDAR Resources](https://www.usgs.gov/3d-elevation-program/3dep/state-solicitations) - Index of state-managed LiDAR programs across the US
- [Point Cloud Processing in Python](https://python-pcl-library.github.io/) - Library for working with LiDAR data programmatically
""",
    "/home/tngai/data/Tutorials/_tutorials/multispectral-imagery.md": """## Introduction

Multispectral imagery captures data at specific wavelengths across the electromagnetic spectrum—beyond what the human eye can see. While a regular photograph records red, green, and blue light (the visible spectrum), multispectral sensors record additional bands: near-infrared, shortwave infrared, and thermal energy. Each band reveals different information about the Earth's surface. Healthy vegetation, for instance, reflects strongly in near-infrared but absorbs red light (how plants photosynthesize), making the difference between these bands a powerful indicator of plant health.

The satellites carrying these sensors—Landsat, Sentinel, MODIS—have been observing Earth systematically since the 1970s. This creates an extraordinary archive: you can compare how a site looked in 1990 versus today, track deforestation patterns, measure urban growth, or assess flood extents. For designers, this historical perspective reveals site dynamics that a single site visit cannot—seasonal flooding patterns, long-term erosion, or gradual changes in land cover.

The power of multispectral analysis lies in band combinations. By combining different spectral bands, you can create images tailored to specific questions. Color infrared imagery (displaying near-infrared as red) makes vegetation "glow" red, instantly revealing plant health and density. False-color urban imagery highlights built structures and bare soil. Bathymetric combinations can peer through shallow water to map underwater features. The same raw data becomes many different analytical tools depending on how you combine and display the bands.

## Historical Context

The first civilian Earth observation satellite, Landsat 1, launched in 1972 with a four-band multispectral scanner. This revolutionary mission proved that satellites could consistently monitor Earth's surface and made remote sensing data publicly available. The program has continued uninterrupted through Landsat 8 (launched 2013) and Landsat 9 (2021), creating a nearly 50-year unbroken record of Earth's land surface.

Meanwhile, European Space Agency's Sentinel program, part of the Copernicus initiative, began launching in 2014, providing free, high-quality data with frequent revisit times (Sentinel-2 passes the same location every 5 days). This temporal resolution transformed what's possible for monitoring rapid changes—floods, fires, agricultural cycles.

The US government made a pivotal decision in 2008 to make Landsat data free, sparking an explosion in applications and analysis. Combined with increasingly powerful and accessible processing tools like QGIS, Google Earth Engine, and Python's rasterio library, multispectral analysis moved from government agencies and research institutions to anyone with a computer and curiosity.

## Design Relevance

Multispectral imagery provides site designers with analytical capabilities that complement and extend traditional site analysis methods. Understanding vegetation health across a site, for instance, reveals microclimates—areas of stress may indicate poor soil conditions, drainage problems, or areas lacking irrigation. This helps prioritize intervention zones or understand why certain areas developed naturally as habitat corridors.

Land cover classification using multispectral data quantifies what site visit observations can only estimate qualitatively. How much of the site is impervious surface versus vegetated? What type of vegetation exists—forest, grassland, wetland? These questions have direct implications for stormwater management, ecological connectivity, and heat island mitigation strategies.

The historical archive of satellite imagery enables longitudinal analysis impossible through site visits alone. You can identify seasonal water patterns that might indicate flood zones, track how neighboring developments changed the landscape over time, or discover that what appears to be undisturbed forest was actually farmland two decades ago. This temporal dimension supports design decisions grounded in site history rather than snapshot observations.

Thermal bands reveal heat patterns across the landscape—where buildings and pavement store and radiate heat, how tree canopy coverage affects local temperatures, which slopes receive sun exposure at different times of day. Combined with building footprint data, this enables urban heat island mitigation strategies that target the most impactful interventions.

## Resources & Further Reading

- [USGS Landsat Mission](https://www.usgs.gov/landsat-missions/landsat-satellites) - Comprehensive information on Landsat satellites, data access, and band specifications
- [EOS.com Landsat 8 Band Combinations](https://eos.com/make-an-analysis/landsat-8-bands-combinations/) - Practical guide to common band combinations and their applications
- [QGIS Documentation: Raster Analysis](https://docs.qgis.org/latest/en/docs/user_manual/working_with_raster/raster_analysis.html) - Official guide to processing multispectral data in QGIS
- [Copernicus SciHub](https://scihub.copernicus.eu/) - Access to Sentinel satellite data from the European Space Agency
- [NASA Earth Observatory: Measuring Vegetation](https://earthobservatory.nasa.gov/features/MeasuringVegetation) - Accessible introduction to NDVI and vegetation indices
""",
    "/home/tngai/data/Tutorials/_tutorials/photogrammetry.md": """## Introduction

Photogrammetry is the science of making measurements from photographs—specifically, deriving 3D positions of points from overlapping 2D images. When you take many overlapping photos of an object or scene from different angles, software can identify matching points across images and triangulate their positions in 3D space. The result is a point cloud or mesh that precisely represents the photographed subject's shape. For designers, this means you can digitize almost anything with a camera: a building facade, a sculpture, an urban streetscape, an archaeological artifact.

The key insight behind photogrammetry is parallax—the apparent shift of an object's position when viewed from different angles. If you see a building from the left side, the windows appear at one position relative to the building's corner. From the right side, they appear shifted. By calculating these shifts across many overlapping images, software reconstructs the 3D geometry. Modern photogrammetric algorithms, particularly Structure from Motion (SfM), automate this process, handling thousands of images and millions of points with minimal human intervention.

Reality Capture, the software used in this tutorial, represents the current state of the art in accessible photogrammetry. It can process images from smartphones, DSLRs, or specialized survey cameras, producing point clouds, meshes, and textured models suitable for visualization, analysis, or fabrication. The software leverages GPU acceleration to achieve processing speeds that were unthinkable a decade ago.

## Historical Context

Photogrammetry began with aerial photography in the late 19th century. Surveyors discovered that overlapping photographs taken from aircraft could be viewed in stereo to extract elevation information—pioneering the mapping method that produced topographic maps for decades. The stereoscope, still used today, exploits the brain's natural ability to fuse two offset images into a single 3D perception.

The digital revolution transformed photogrammetry from an analog to computational discipline. Early digital photogrammetry required expensive specialized hardware and expertise. The critical breakthrough came with "Structure from Motion" algorithms in the 2000s, which automated feature matching across images without requiring pre-calibrated camera positions. This made photogrammetry accessible to anyone with a camera.

The 2010s saw photogrammetry migrate from specialized applications to mainstream design and entertainment. Game studios, VFX houses, and architects adopted the technology for asset creation and existing conditions documentation. Epic Games' acquisition of Reality Capture signals the technology's value for real-time visualization and metaverse applications.

Simultaneously, hardware evolved: higher resolution sensors, better lens quality, and the ubiquity of GPS-tagged images all improved data quality. Today's smartphones capture images detailed enough for professional-grade photogrammetry, removing the barrier of specialized equipment.

## Design Relevance

Photogrammetry offers designers a direct bridge between physical site conditions and digital design tools. A site visit supplemented with hundreds of overlapping photographs yields a 3D model accurate enough for measuring distances, extracting elevations, or testing design interventions against existing geometry. This is especially valuable for historic preservation projects where existing conditions may be poorly documented.

The technology democratizes 3D scanning. Traditional terrestrial LiDAR scanners cost tens to hundreds of thousands of dollars; photogrammetry requires only a camera (often a smartphone) and processing software. Reality Capture's educational licensing makes this capability accessible to students, enabling workflows previously limited to well-funded research labs or large firms.

For urban design and landscape architecture, photogrammetry enables detailed existing conditions documentation at scales from street furniture to neighborhood character. Combined with drone imagery, it can capture sites inaccessible by foot or too large for ground-based photography alone. The resulting point clouds or meshes become base maps for further analysis or visualization.

The entertainment industry applications—game assets, VFX, virtual production—represent a growing design domain where photogrammetry skills transfer directly. Understanding the workflow, including proper photography techniques, control point usage, and mesh optimization, prepares students for careers spanning architecture, gaming, film, and immersive media.

## Resources & Further Reading

- [Reality Capture Education](https://www.capturingreality.com/Education) - Official tutorials and educational licensing information
- [Photogrammetry Wikipedia](https://en.wikipedia.org/wiki/Photogrammetry) - Comprehensive overview of principles and applications
- [Sketchfab Blog: Photogrammetry Best Practices](https://sketchfab.com/blogs-category/tutorial) - Practical tips for photographing objects and scenes
- [Agisoft Metashape Documentation](https://agisoft.com/support/documentation/) - Alternative photogrammetry software with extensive tutorials
- [Epic Games Reality Capture](https://www.epicgames.com/store/en-US/product/reality-capture) - Information on Reality Capture by its current owner
""",
    "/home/tngai/data/Tutorials/_tutorials/land-cover.md": """## Introduction

Land cover classification categorizes the Earth's surface into types: forest, grassland, agriculture, developed/urban, water, wetlands, and more. Unlike land use (what humans do with the land—residential, commercial, park), land cover describes the physical surface. A baseball field and a parking lot might both be "developed" land cover, but they have very different implications for stormwater, heat, and ecology. This distinction matters for design: understanding actual surface conditions informs drainage design, microclimate intervention, and habitat connectivity.

Land cover data comes primarily from satellite imagery analysis. The USDA's National Land Cover Database (NLCD), updated every few years, provides 30-meter resolution classification for the entire US. More detailed data exists for some regions—1-meter resolution for certain urban areas—but the NLCD offers unmatched consistency and historical depth, with versions going back to 1992. This allows designers to understand not just current conditions, but how the landscape has changed—where forest has been lost to development, where agriculture has expanded, where urban areas have densified.

For site-scale analysis, land cover data provides baseline context. A proposed development adjacent to a large forested area needs different stormwater and wildlife mitigation than one surrounded by other urban uses. Regional land cover analysis quantifies impervious surface percentages, vegetation coverage, and connectivity patterns that inform both site design and policy recommendations.

## Historical Context

Systematic land cover mapping began with the USGS in the 1970s, leveraging the same aerial photography and early satellite data used for topographic mapping. The Corine Land Cover program, initiated by the European Community in 1985, established standardized classification systems still referenced today. In the US, the USGS GAP (Gap Analysis Program) created the first comprehensive national land cover dataset in the 1990s.

The 2000s saw major advances with the NLCD, a collaborative effort producing consistent wall-to-wall coverage for the US. The 30-meter resolution (each pixel represents 30x30 meters on the ground) comes from Landsat satellite imagery, chosen as a practical balance between detail and manageable data volume. Earlier datasets had coarser resolution—1-kilometer pixels in global products—limiting their utility for local planning.

Contemporary land cover classification increasingly uses machine learning algorithms that automatically identify patterns in multispectral imagery. These methods achieve accuracy levels difficult to attain through manual interpretation alone, and they scale to continental or global datasets. The European Copernicus program produces global land cover maps annually, while initiatives like Microsoft's Planetary Computer provide access to petabytes of analysis-ready environmental data.

## Design Relevance

Land cover directly affects environmental performance of designed systems. Impervious surfaces—roads, rooftops, parking lots—prevent rainwater infiltration, increasing runoff volumes and velocities, concentrating pollutants, and degrading aquatic habitats. Knowing the percentage of impervious cover in a watershed helps size stormwater management infrastructure and predict downstream flooding risks.

The urban heat island effect correlates strongly with land cover: areas with less vegetation and more dark, absorptive surfaces run significantly hotter. Land cover analysis identifies heat-vulnerable neighborhoods and targets locations for tree planting, green roofs, or cool pavement interventions. This spatial targeting improves the cost-effectiveness of heat mitigation investments.

Ecological connectivity depends on continuous vegetated corridors, which land cover analysis can map and quantify. A site within a fragmented landscape may need wildlife crossings or vegetated buffer zones to maintain ecological function. Understanding the larger landscape context prevents designs that inadvertently isolate habitat patches or sever movement corridors.

For urban design and landscape architecture, land cover classification provides defensible baselines for master planning. Showing clients and regulators how their site contributes to or mitigates regional impervious surface percentages, canopy loss, or habitat fragmentation grounds design recommendations in measurable environmental performance rather than aesthetic preference alone.

## Resources & Further Reading

- [USDA MRLC Consortium](https://www.mrlc.gov/) - Access to NLCD data and related land cover resources
- [USGS Gap Analysis Project](https://www.usgs.gov/programs/gap-analysis-project) - LANDFIRE vegetation data and species habitat modeling
- [EPA EnviroAtlas](https://www.epa.gov/enviroatlas) - Interactive tool combining land cover with environmental and health indicators
- [UMass DSL: Designing Sustainable Landscapes](https://umassdsl.org/) - Ecological framework linking landscape design to habitat connectivity
- [Census Bureau TIGER/Line Data](https://www.census.gov/cgi-bin/geo/shapefiles/index.php) - Urban area boundaries and demographic data to combine with land cover analysis
""",
    "/home/tngai/data/Tutorials/_tutorials/sea-level-rise.md": """## Introduction

Sea level rise is one of the most consequential consequences of climate change, threatening coastal infrastructure, freshwater resources, and ecosystems worldwide. As greenhouse gases warm the atmosphere, two things happen: water expands (thermal expansion, accounting for roughly half of observed rise), and ice sheets in Greenland and Antarctica melt faster than they accumulate snowfall. The result is seas that have risen approximately 8-9 inches globally since 1900, with the rate accelerating—from about 0.06 inches per year in the early 20th century to nearly 0.14 inches per year today.

For coastal designers—architects, landscape architects, urban planners—the implications are profound. Buildings sited in flood zones face increasing insurance costs and regulatory requirements. Infrastructure designed for historical flood elevations may become inadequate. Waterfront parks and public spaces may require adaptive redesign or managed retreat. Understanding sea level rise projections and their spatial implications transforms how coastal sites are conceived and programmed.

This tutorial focuses on visualizing sea level rise using Digital Elevation Models—essentially asking "if the water were this high, what would be flooded?" This "bathtub" approach provides a first-order assessment useful for strategic planning and communication. More sophisticated models account for storm surge, wave action, and hydrodynamic processes, but DEM-based visualization effectively conveys the stakes and scope of the challenge.

## Historical Context

Tide gauge records extending back to the 1700s in some locations document long-term sea level trends, revealing that sea level has risen approximately 120 meters since the last glacial maximum 20,000 years ago. These geological timescales provide context but also indicate the pace of change: the rate currently observed is extremely rapid by geological standards.

Modern sea level research accelerated with satellite altimetry missions beginning in the early 1990s. The TOPEX/Poseidon satellite, launched in 1992, provided the first precise, continuous measurements of global sea surface height, revealing variations and trends invisible to tide gauges. Subsequent missions (Jason series, Sentinel-6) continue this record, providing the data underlying current projections.

The IPCC (Intergovernmental Panel on Climate Change) produces periodic assessment reports synthesizing sea level research. The Sixth Assessment Report (2021) projects global mean sea level rise of 0.3 to 1.0 meters by 2100 under various emissions scenarios, with higher end estimates incorporating potential ice sheet instabilities. These projections inform building codes, infrastructure planning, and coastal zoning in many jurisdictions.

NOAA's Sea Level Rise Viewer and similar tools make projection data accessible for local planning, allowing communities to visualize which areas become inundated under different scenarios. Many coastal cities have incorporated these visualizations into comprehensive plans and hazard mitigation strategies.

## Design Relevance

Coastal flooding from sea level rise compounds existing storm surge risks. A 100-year flood event—one with a 1% chance of occurring in any year—becomes more frequent as base sea level rises: what was a 100-year flood might become a 10-year flood by mid-century. For designers, this means building envelope, foundation, and mechanical system decisions that once assumed historical flood elevations may require reassessment.

Beyond flooding, sea level rise threatens coastal groundwater tables. As seas rise, the freshwater-saltwater interface moves inland and upward. Buildings with basements or below-grade structures may encounter brackish or saltwater intrusion, affecting foundation integrity and indoor air quality. Landscape designs relying on freshwater irrigation may face increasing constraints.

Adaptation strategies fall into three categories: protection (hard infrastructure like seawalls, soft infrastructure like dunes and marshes), accommodation (building designs that tolerate periodic flooding), and retreat (relocating development away from vulnerable areas). Each approach involves tradeoffs between cost, effectiveness, ecological impact, and social equity. Designers must understand these tradeoffs to advise clients and communities realistically.

Visualization is a critical design tool for sea level rise communication. Converting DEM data into inundation maps transforms abstract projections into tangible site conditions. These visualizations support community engagement, grant applications, regulatory discussions, and the design process itself—helping stakeholders understand what is at stake before committing to adaptation strategies.

## Resources & Further Reading

- [NOAA Sea Level Rise Viewer](https://coast.noaa.gov/slr/) - Interactive tool for visualizing sea level rise and flood scenarios along US coasts
- [NOAA Digital Coast Data](https://coast.noaa.gov/digitalcoast/) - Download sea level rise data, coastal elevation models, and wetland impact projections
- [IPCC AR6 Sea Level Projections](https://www.ipcc.ch/report/ar6/wg1/) - Authoritative scientific projections of sea level rise under different emissions scenarios
- [Climate Central Surging Seas](https://riskfinder.climatecentral.org/) - Locally-specific sea level rise and flood risk analysis
- [USACE Sea Level Rise Calculator](https://www.usace.army.mil/corpscope/) - Engineering guidance for incorporating sea level rise into coastal project design
""",
    "/home/tngai/data/Tutorials/_tutorials/urban-heat-island-effect.md": """## Introduction

The Urban Heat Island (UHI) effect describes how cities and urban areas are significantly warmer than surrounding rural areas—sometimes by 5-10°F or more during summer heat events. This happens because urban materials—dark asphalt, concrete, roofing membranes—absorb solar radiation during the day and release it slowly at night, creating heat reservoirs. Vegetation and trees, which cool the environment through evapotranspiration, are typically sparse in cities. The result is not just higher average temperatures, but extreme heat events that pose public health risks, increase energy demand for cooling, and accelerate air pollution formation.

For designers, UHI is both a challenge and an opportunity. Dense urban areas with abundant dark surfaces and little shade can become dangerously hot—contributing to heat-related illness and mortality, especially in neighborhoods lacking air conditioning or with populations vulnerable to heat stress. But the built environment also shapes heat patterns: building orientation, street width, tree canopy coverage, surface materials, and vegetation all affect how heat accumulates and dissipates. Thoughtful design can mitigate heat island effects and create more comfortable outdoor spaces.

This tutorial uses Landsat 8 thermal imagery to estimate Land Surface Temperature (LST)—not air temperature, but how hot surfaces actually become. LST reveals which materials and locations store the most heat, information designers can use to target interventions: where to add shade trees, which surfaces to change, how building orientation affects pedestrian comfort.

## Historical Context

Scientists first documented urban-rural temperature differences in the early 1800s, noticing that cities were warmer than countryside. Luke Howard's 1818 study of London's climate identified the "heat island" phenomenon, noting that nighttime temperatures in the city center remained elevated even as surrounding areas cooled.

Systematic study accelerated in the mid-20th century as cities grew and thermal imaging technology emerged. Researchers in the 1950s and 1960s mapped Chicago, Tokyo, and other major cities, documenting temperature variations across urban transects. The Environmental Protection Agency formally studied UHI in the 1970s and 1980s, establishing the scientific basis for mitigation policies.

Satellite-based UHI research began with early Landsat missions in the 1970s, but thermal sensors with sufficient resolution for urban analysis came online with Landsat 4 (1982) and improved significantly with Landsat 7 (1999) and Landsat 8 (2013). The Landsat archive now spans over 40 years, enabling long-term studies of how urban heat patterns have intensified with development.

Contemporary research links UHI to environmental justice: historically marginalized neighborhoods often have less tree canopy, more industrial land uses, and older buildings with less insulation—all contributing to higher temperatures. Studies in cities like Phoenix, Baltimore, and Houston have documented that heat vulnerability maps onto existing patterns of social and racial inequality, motivating equity-focused design interventions.

## Design Relevance

Designers increasingly must consider thermal comfort as a performance criterion, not just an aesthetic one. Heat exposure affects how people use outdoor spaces—whether a plaza is habitable at noon in August, whether children can safely walk to school, whether elderly residents can garden without risk. Tools like Universal Thermal Climate Index (UTCI) and others attempt to quantify thermal comfort, but Landsat-derived LST provides accessible, locally-specific baseline data.

Cool surfaces—light-colored roofing, reflective pavement coatings, shade structures—reduce heat absorption and lower surface temperatures. Green infrastructure—trees, green roofs, parks—provides shade and evaporative cooling. Both strategies can significantly reduce local temperatures, but their effectiveness varies by context: a green roof cools the building it sits on more than the surrounding air, while a large park can cool adjacent neighborhoods through airflow and evapotranspiration.

Vegetation mapping using NDVI (Normalized Difference Vegetation Index) from multispectral imagery reveals which areas have tree canopy and which lack it. Overlaying vegetation maps with LST maps identifies mismatches: neighborhoods with both high temperatures and low canopy coverage are prime candidates for tree planting programs. This spatial targeting improves the return on greening investments.

Material selection matters at multiple scales. At the building scale, cool roofing and walls reduce cooling loads and lower surface temperatures. At the neighborhood scale, permeable pavement, tree trenches, and pocket parks cumulatively affect thermal comfort. Designers who understand these relationships can advocate for material palettes and site designs that mitigate rather than exacerbate heat islands.

## Resources & Further Reading

- [EPA Heat Island Effect](https://www.epa.gov/heatislands) - Comprehensive overview of UHI causes, impacts, and mitigation strategies
- [USGS Landsat 8 Surface Temperature](https://www.usgs.gov/landsat-missions/landsat-8) - Technical details on thermal band calibration and temperature derivation
- [Tree Equity](https://treeequity.org/) - Interactive mapping tool connecting tree canopy coverage to socioeconomic data
- [NOAA Heat Health Tools](https://www.noaa.gov/heat-health) - Weather service resources for heat event planning and response
- [Landscape Architecture Foundation Heat Briefs](https://www.lafoundation.org/research/heat-briefs) - Design-focused resources on heat mitigation strategies with case studies
""",
    "/home/tngai/data/Tutorials/_tutorials/solar-potential.md": """## Introduction

Solar potential analysis assesses how much sunlight a site, building, or surface can receive and convert into usable energy or daylight. This assessment involves understanding both the solar resource itself (how much energy arrives from the sun) and site-specific factors that modify it (shading from topography, trees, or buildings; surface orientation and tilt; atmospheric conditions). For designers, solar analysis informs passive solar design, photovoltaic system sizing, daylighting strategies, and outdoor thermal comfort.

The sun delivers approximately 1,000 watts per square meter to Earth's surface under ideal clear-sky conditions at sea level. This "solar constant" doesn't vary—the Earth's orbit is nearly circular and stable on human timescales. What varies is how much of this resource reaches a given location and surface: latitude affects the angle of incoming radiation; atmosphere (clouds, pollution, humidity) absorbs and scatters light; terrain and structures create shadows; surface orientation determines exposure.

Designers work with two key metrics. Global Horizontal Irradiance (GHI) measures total solar radiation on a horizontal surface, including direct sunlight and diffuse sky radiation. Direct Normal Irradiance (DNI) measures only the direct beam from the sun, relevant for concentrator systems like those on solar trackers. Understanding both helps size and orient systems appropriately.

## Historical Context

Humans have harnessed solar energy for millennia—orienting buildings to capture winter sun, drying crops, heating water in passive systems. The modern scientific study of solar radiation began in the 19th century, with researchers measuring solar output and atmospheric effects systematically.

The photovoltaic effect, discovered in 1839 by Edmond Becquerel, was theoretical until the 1950s when Bell Labs produced the first practical silicon solar cell. Early photovoltaics were extremely expensive, used primarily for space satellites. The 1970s oil crisis sparked research into terrestrial applications, but costs remained prohibitive.

A remarkable cost decline changed everything: solar module prices fell from over $70 per watt in 1975 to under $0.30 per watt today. This 99% reduction, driven by manufacturing scale, technology improvements, and policy incentives, made solar competitive with fossil fuels in many markets. Today, solar is the fastest-growing electricity source globally.

The National Renewable Energy Laboratory (NREL) has been measuring and modeling solar resources since the 1970s, establishing the scientific basis for solar deployment. Their National Solar Radiation Database, with over 1,400 monitoring stations across the US, provides the data underlying solar potential assessments.

## Design Relevance

Building orientation and window placement, informed by solar analysis, can dramatically reduce energy consumption. A building that captures winter sun (when the sun is low and heating is welcome) while shading windows in summer (when the sun is high and cooling loads are highest) reduces both heating and cooling demands. This passive solar design has been practiced for millennia—the Pantheon in Rome, the solar houses of Eleanor and Raymond Fick—but systematic solar analysis tools now make it accessible to any designer.

Photovoltaic system design requires accurate solar potential assessment. Oversizing systems wastes money; undersizing leaves rooftop potential unrealized. Solar analysis tools model shading from nearby buildings and trees across all seasons, producing annual generation estimates accurate enough for financial projections. Tools like NREL's PVWatts calculator make this accessible without specialized expertise.

Urban design implications extend beyond individual buildings. Street orientation affects solar access for pedestrians; park placement affects neighborhood cooling; building height limits affect shadowing on adjacent properties. Some jurisdictions have enacted solar rights legislation or daylighting codes protecting solar access, making basic solar analysis relevant to planning and zoning decisions.

Daylighting—using sunlight to illuminate building interiors—reduces electricity consumption while providing connection to outdoor conditions. Understanding solar paths, window placement, and light shelf design enables daylighting strategies that balance visual comfort, thermal gains, and glare control. The same solar analysis that informs photovoltaics enables better daylighting design.

## Resources & Further Reading

- [NREL National Solar Radiation Database](https://www.ncei.noaa.gov/products/land-based-station/national-solar-radiation-database) - Free historical solar radiation data for over 1,400 US stations
- [NREL PVWatts Calculator](https://pvwatts.nrel.gov/) - Online tool for estimating photovoltaic system energy production
- [NREL Solar Resource Data](https://www.nrel.gov/gis/solar-resource.html) - Overview of solar data sources and tools from NREL
- [FEMP Solar Analysis Tools](https://www.energy.gov/femp/solar-analysis-tools) - Federal energy management program guidance on solar assessment
- [SUNY ESF Solar Resource Guide](https://www.esf.edu/solar/) - Educational resources explaining solar radiation concepts and measurement
""",
    "/home/tngai/data/Tutorials/_tutorials/indexed-image.md": """## Introduction

Indexed image analysis uses mathematical combinations of spectral bands—called vegetation indices—to highlight specific features or conditions. The most famous is NDVI (Normalized Difference Vegetation Index), which exploits the fact that healthy vegetation absorbs red light for photosynthesis while reflecting near-infrared. By comparing these two bands, NDVI quantifies vegetation health and density across entire landscapes. Other indices serve different purposes: NDWI (Normalized Difference Water Index) highlights open water; NDSI (Normalized Difference Snow Index) detects snow cover; NDMI (Normalized Difference Moisture Index) indicates surface moisture content.

The power of indices lies in their ability to transform raw spectral data into meaningful measurements. A red pixel in a satellite image could be soil, rooftop, or dead vegetation—NDVI disambiguates these. A bright pixel in thermal data indicates high temperature, but surface temperature varies with material type regardless of ambient conditions. Indices condense multidimensional spectral information into single values that map directly to real-world conditions.

For design applications, vegetation indices provide spatially explicit information about landscape conditions that would be impossible to gather through field observation alone. NDVI maps reveal which urban neighborhoods have tree canopy and which lack it—a foundation for environmental justice analysis and equitable greening strategies. Time-series NDVI shows whether vegetation is recovering after a development project or declining under stress.

## Historical Context

The scientific foundation for vegetation indices was established in the 1970s with the launch of Landsat 1. Researchers noticed that the ratio of near-infrared to red reflectance distinguished vegetation from other surfaces, and various indices were proposed. NDVI, introduced in 1973 by Donald R. Tilley and colleagues, became the most widely used.

The index was refined as understanding of plant spectral properties improved. The core principle—that photosynthetically active vegetation uniquely absorbs red while reflects near-infrared—stays constant, but normalization methods and threshold calibrations evolved. NDVI values range from -1 to +1, with higher values indicating denser, healthier vegetation.

Advanced indices continue to be developed. The Enhanced Vegetation Index (EVI) addresses NDVI saturation in dense canopies. The Normalized Difference Moisture Index (NDMI) emerged as thermal and shortwave infrared bands became available. Each new satellite mission adds spectral bands enabling finer discrimination—Landsat 8's coastal aerosol band improves water quality assessment, for instance.

Today, vegetation indices are standard tools in precision agriculture, forest management, drought monitoring, and urban planning. Google Earth Engine and similar platforms provide access to global NDVI and other indices computed from decades of satellite data, enabling analysis impossible when indices had to be computed from individual scenes.

## Design Relevance

NDVI maps serve as quantitative baselines for landscape assessment. Where a site visit reveals "some trees," NDVI reveals exactly how much vegetation exists, where it's concentrated, and how healthy it is. This matters for both impact assessment (how will this project affect urban tree canopy?) and opportunity identification (which neighborhoods would benefit most from greening investments?).

Time-series NDVI analysis reveals landscape dynamics invisible in static images. Comparing NDVI from different years shows whether urban tree canopy is growing or shrinking, whether post-fire vegetation recovery is progressing, whether agricultural land is being converted to development. For designers working on long-term projects, understanding these trajectories informs recommendations that account for future conditions, not just present ones.

Water indices (NDWI, MNDWI) complement vegetation analysis. Urban streams often have complex surface water signatures—polluted water reflects differently than clean water, drained wetlands look different from flooded ones. Combined with land cover classification, water indices help designers understand the hydrological context: where does stormwater originate, where does it flow, what ecosystems depend on surface water?

Indices derived from Landsat and Sentinel data are free and globally available, making sophisticated environmental analysis accessible without expensive field campaigns. Design studios can integrate NDVI analysis into site assessment using only QGIS and publicly available satellite imagery, producing deliverables that previously required specialized remote sensing expertise.

## Resources & Further Reading

- [NASA Earth Observatory: Measuring Vegetation](https://earthobservatory.nasa.gov/features/MeasuringVegetation) - Accessible introduction to NDVI and its applications
- [EOS.com NDVI Guide](https://eos.com/make-an-analysis/ndvi/) - Practical guide to using NDVI for vegetation assessment
- [USGS Remote Sensing FAQ](https://www.usgs.gov/faqs/what-remote-sensing) - Answers common questions about satellite imagery and indices
- [Sentinel Hub EO Browser](https://www.sentinel-hub.com/explore/eobrowser/) - Free tool for exploring multispectral indices from Sentinel satellites
- [Index Database](https://www.indexdatabase.de/) - Comprehensive catalog of vegetation indices and their applications
""",
}


def insert_sections(filepath, new_sections):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    first_dash = content.find("---")
    if first_dash == -1:
        print(f"ERROR: No frontmatter found in {filepath}")
        return False

    second_dash = content.find("---", first_dash + 1)
    if second_dash == -1:
        print(f"ERROR: Frontmatter malformed in {filepath}")
        return False

    insertion_point = second_dash + 3

    if content[insertion_point : insertion_point + 1] == "\n":
        insertion_point += 1

    new_content = (
        content[:insertion_point]
        + "\n"
        + new_sections
        + "\n"
        + content[insertion_point:]
    )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Modified: {filepath}")
    return True


def main():
    success_count = 0
    for filepath in TUTORIALS:
        if insert_sections(filepath, TUTORIALS[filepath]):
            success_count += 1

    print(f"\n{success_count}/{len(TUTORIALS)} files modified successfully.")


if __name__ == "__main__":
    main()
