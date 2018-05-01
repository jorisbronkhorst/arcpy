#env.workspace = r"\\enc-cap-iba-03\IBA03_GIS\GIS_connecties\productie_analisten\DC - PADWH2 - DM_ESRI_KIJK.sde"

arcpy.env.workspace = r"C:\Users\604251\Documents\ArcGIS\Default.gdb"
mxd = arcpy.mapping.MapDocument("CURRENT")

arcpy.mapping.AddLayer(arcpy.mapping.ListDataFrames(mxd)[0], arcpy.mapping.Layer("Leidingen"))
Leidingen = arcpy.mapping.ListLayers(mxd, 'Leidingen')[0]
Leidingen.definitionQuery = "STATUS_BEHEER = 'In bedrijf' AND ACTUEEL = 'J'"

arcpy.mapping.AddLayer(arcpy.mapping.ListDataFrames(mxd)[0], arcpy.mapping.Layer("Afsluiters"))
Afsluiters = arcpy.mapping.ListLayers(mxd, 'Afsluiters')[0]
Afsluiters.definitionQuery = "STATUS_BEHEER = 'In bedrijf' AND ACTUEEL = 'J'"

arcpy.mapping.AddLayer(arcpy.mapping.ListDataFrames(mxd)[0], arcpy.mapping.Layer("Stations"))
Stations = arcpy.mapping.ListLayers(mxd, 'Stations')[0]
Stations.definitionQuery = "STATUS_BEHEER = 'In bedrijf' AND ACTUEEL = 'J'"

arcpy.mapping.AddLayer(arcpy.mapping.ListDataFrames(mxd)[0], arcpy.mapping.Layer("T_stukken"))
T_stukken = arcpy.mapping.ListLayers(mxd, 'T_stukken')[0]
T_stukken.definitionQuery = "STATUS_BEHEER = 'In bedrijf' AND ACTUEEL = 'J'"

arcpy.SpatialJoin_analysis("T_stukken", "afsluiters", "T_join", match_option = "WITHIN_A_DISTANCE", search_radius = 2.5, field_mapping = "COUNT")

T_join = arcpy.mapping.Layer('T_join')
T_join.definitionQuery = "Join_Count = '3'"

arcpy.SelectLayerByLocation_management("afsluiters", "WITHIN_A_DISTANCE", "T_join", search_distance = 2.5, selection_type = "NEW_SELECTION")
arcpy.CopyFeatures_management("afsluiters", "afsluiter_selectie")


#arcpy.MakeFeatureLayer_management('DM_ESRI.G_STATION_PUNTEN', 'stations')
#stations = arcpy.mapping.Layer('stations')
#stations.definitionQuery = "STATUS_BEHEER = 'In bedrijf' AND ACTUEEL = 'J'"


#T_cursor = arcpy.da.SearchCursor(T_stukken, ['BRON_ID', 'SHAPE@'])
#T_lijst = [row for row in T_cursor]
#T_buffered = [x[1].buffer(2) for x in T_lijst]
#arcpy.CopyFeatures_management(T_buffered)

arcpy.Buffer_analysis("T_stukken", buffer_distance_or_field = 2)
# maak count value van 1 bij de punten en doe spatial join vanaf de buffer zones met SUM

#T_stuk_gebied_cursor = arcpy.da.SearchCursor("T_stuk_gebied", ["OID@", "SHAPE@"])
#T_stuk_gebied_lijst = [row for row in T_stuk_gebied_cursor]

#data = {}
#... for gebied in T_stuk_gebied_lijst[0:10]:
#...     arcpy.SelectLayerByLocation_management("Afsluiters_selectie", select_features = gebied[1])
#...     count = int(arcpy.GetCount_management("Afsluiters_selectie").getOutput(0))
#...     data[gebied[0]] = count

#arcpy.SelectLayerByLocation_management("leidingen", "INTERSECT", T_stuk_lijst[2][1], search_distance = 0.1, selection_type = "NEW_SELECTION")

#T_stuk_cursor = arcpy.da.SearchCursor("T_stukken", ["BRON_ID", "SHAPE@"])
#T_stuk_lijst = [row for row in T_stuk_cursor]

