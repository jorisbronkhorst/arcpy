#from __future__ import division

# workspace and mapdocument definiëren
arcpy.env.workspace = r"C:\Users\604251\Documents\ArcGIS\Default.gdb"
mxd = arcpy.mapping.MapDocument("CURRENT")

# laad T_stukken en Leidingen als laag in het eerste dataframe van het mapdocument
arcpy.mapping.AddLayer(arcpy.mapping.ListDataFrames(mxd)[0], arcpy.mapping.Layer("T_stukken"))
T_stukken = arcpy.mapping.ListLayers(mxd, "T_stukken")[0]

arcpy.mapping.AddLayer(arcpy.mapping.ListDataFrames(mxd)[0], arcpy.mapping.Layer("Leidingen"))
Leidingen = arcpy.mapping.ListLayers(mxd, "Leidingen")[0]

# zet definitiequery van T_stukken en Leidingen (maximaal lengte 2, want we zoeken afsluiters op max afstand van 2 tot afsluiter)
T_stukken.definitionQuery = "STATUS_BEHEER = 'In bedrijf' AND ACTUEEL = 'J'"

Leidingen.definitionQuery = "STATUS_BEHEER = 'In bedrijf' AND ACTUEEL = 'J' AND LENGTE <= 2"

# selecteer de leidingstukken verbonden met een T_stuk en maak daar een nieuwe laag van
arcpy.SelectLayerByLocation_management("Leidingen", "INTERSECT", "T_stukken", selection_type = "NEW_SELECTION")
arcpy.CopyFeatures_management("Leidingen", "Leidingen_selectie")
Leidingen_selectie = arcpy.mapping.ListLayers(mxd, "Leidingen_selectie")[0]

Leidingen.visible = False

# laad Afsluiters als laag in het eerste dataframe van het mapdocument
arcpy.mapping.AddLayer(arcpy.mapping.ListDataFrames(mxd)[0], arcpy.mapping.Layer("Afsluiters"))
Afsluiters = arcpy.mapping.ListLayers(mxd, "Afsluiters")[0]

# zet definitiequery van Afsluiters
Afsluiters.definitionQuery = "STATUS_BEHEER = 'In bedrijf' AND ACTUEEL = 'J' AND FUNCTIE = 'Onbekend'"

# pak van de geselecteerde leidingstukken de stukken waar een afsluiter aan vast zit en maak er een nieuwe laag van
arcpy.SelectLayerByLocation_management("Leidingen_selectie", "INTERSECT", "Afsluiters", selection_type = "NEW_SELECTION")
arcpy.CopyFeatures_management("Leidingen_selectie", "Leidingen_selectie_met_AFS")
Leidingen_selectie_met_AFS = arcpy.mapping.ListLayers(mxd, "Leidingen_selectie_met_AFS")[0]

Leidingen_selectie.visible = False

# doe een spatiale join van de T_stukken en de leidingen aan een T stuk met een afsluiter
arcpy.SpatialJoin_analysis("T_stukken", "Leidingen_selectie_met_AFS", "T_stuk_leiding_met_AFS_join", match_option = "INTERSECT")
T_stuk_leiding_met_AFS_join = arcpy.mapping.ListLayers(mxd, "T_stuk_leiding_met_AFS_join")[0]

T_stukken.visible = False

# zet definitiequery van de spatiale join om zo de T_stukken te vinden waar 3 afsluiters mee verbonden zijn
T_stuk_leiding_met_AFS_join.definitionQuery = "Join_Count = 3"

# selecteer de leidingstukken die in een groep van 3 verbonden zijn met een T_stuk en waar aan elk een afsluiter zit 
arcpy.SelectLayerByLocation_management("Leidingen_selectie_met_AFS", "INTERSECT", "T_stuk_leiding_met_AFS_join", selection_type = "NEW_SELECTION")
arcpy.CopyFeatures_management("Leidingen_selectie_met_AFS", "Leidingen_selectie_met_AFS_groep")
Leidingen_selectie_met_AFS_groep = arcpy.mapping.ListLayers(mxd, "Leidingen_selectie_met_AFS_groep")[0]

Leidingen_selectie_met_AFS.visible = False
T_stuk_leiding_met_AFS_join.visible = False

# selecteer de afsluiters die in die groep van 3 zitten rondom het T_stuk
arcpy.SelectLayerByLocation_management("Afsluiters", "INTERSECT", "Leidingen_selectie_met_AFS_groep", selection_type = "NEW_SELECTION")
arcpy.CopyFeatures_management("Afsluiters", "Afsluiters_rondom_T_stuk")
Afsluiters_rondom_T_stuk = arcpy.mapping.ListLayers(mxd, "Afsluiters_rondom_T_stuk")[0]

Afsluiters.visible = False
Leidingen_selectie_met_AFS_groep.visible = False

arcpy.RefreshTOC()
arcpy.RefreshActiveView()
# merge with BM GIS and set G inlaat and G uitlaat to NULL in definition query



#Afsluiters_rondom_T_stuk.definitionQuery = "Afsluiters_BM.G_inlaat IS NULL AND Afsluiters_BM.G_inlaat IS NULL"

#arcpy.ExcelToTable_conversion('Afsluiters_BM2.xlsx', 'Afsluiters_BM', "G afsluiter")

#arcpy.AddJoin_management("Afsluiters", "BRON_ID", "Afsluiters_BM", "Id")

