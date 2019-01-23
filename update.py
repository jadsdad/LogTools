from Charts import chartgen_weighted, chartgen_album_weighted
from Reports import catalogue_report, monthly_media_graph, stats_report, yoy_comparison_graph
from TapeCalc import TapeList

chartgen_weighted.run()
chartgen_album_weighted.run()

catalogue_report.main()
monthly_media_graph.run()
stats_report.main()
yoy_comparison_graph.run()

TapeList.generate_report(1.25)