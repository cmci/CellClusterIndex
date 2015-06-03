# cluster index analysis
# ver 1.0 20150423
#
# Kota Miura (miura@embl.de) http://cmci.embl.de
#
# License: GPLv3 (https://www.gnu.org/copyleft/gpl.html)

from fiji.threshold import Auto_Local_Threshold as ALT
from ij.plugin.filter import ParticleAnalyzer as PA
from ij.plugin.filter import EDM, Binary
from ij import IJ, ImagePlus, Prefs
from ij.measure import ResultsTable

Prefs.blackBackground = True

#### Settings to be changed depending on experiment#####
# number of dilate iteration
SAMPLEITER = 5

# load image into memory

#imp3 = ImagePlus('/Users/miura/Dropbox/people/Fukuda/cluster2.tif')
#imp3 = ImagePlus('/Users/miura/Dropbox/people/Fukuda/cluster.tif')
#imp3 = ImagePlus('/Users/miura/Dropbox/people/Fukuda/random.tif')
imp3 = IJ.getImage()

# auto local threshold 
thimp = ALT().exec(imp3, "Bernsen", 20, 0, 0, True)

# watershed to 
edm = EDM()
edm.setup("watershed", None)
edm.run(thimp[0].getProcessor())
#thimp[0].show()
binimp = thimp[0]
binorg = binimp.duplicate()

# Count nucleus setting
MAXSIZE = imp3.getWidth()*imp3.getHeight();
MINSIZE = 100;
#options = PA.SHOW_ROI_MASKS \
#    + PA.EXCLUDE_EDGE_PARTICLES \
#    + PA.INCLUDE_HOLES \
#    + PA.SHOW_RESULTS \

options = PA.INCLUDE_HOLES \
	+ PA.CLEAR_WORKSHEET \
#    + PA.SHOW_RESULTS \    
rt = ResultsTable()
p = PA(options, PA.AREA + PA.STACK_POSITION, rt, MINSIZE, MAXSIZE)
p.setHideOutputImage(True)

# Morphological dilate
binner = Binary()
binner.setup('dilate', None)


clusters = 0
initialCells = 0

# dilate by 'SAMPLEITER'
for i in range(SAMPLEITER+1):
	p.analyze(binimp)
	cellcounts = rt.getCounter()
	if i == 0:
		initialCells = cellcounts
	#IJ.log("iter:" + str(i) + " -- cell counts: " + str(cellcounts))
	if i == SAMPLEITER:
		clusters = cellcounts
	binner.run(binimp.getProcessor())
	rt.reset()

#binimp.show()
#binorg.show()
IJ.log("==== " + imp3.getTitle() + " =====")
IJ.log("Number of Nucleus : " + str(initialCells))
IJ.log("Clusters at dilation " + str(SAMPLEITER) + ": " + str(clusters))
IJ.log("Clusters/Nucleus " + str(float(clusters)/float(initialCells)))

	

