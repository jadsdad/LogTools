from Charts import chartgen_weighted, chartgen_album_weighted
from Reports import catalogue_report, monthly_media_graph, stats_report, yoy_comparison_graph
from TapeCalc import TapeList

print("Creating Charts...")
chartgen_weighted.run()
chartgen_album_weighted.run()

print("Creating Reports...")
stats_report.main()
TapeList.generate_report(1.25)
catalogue_report.main()

print("Creating Graphs...")
monthly_media_graph.run()
yoy_comparison_graph.run()

