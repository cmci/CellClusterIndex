# cluster index analysis
# ver 1.0 20150423
# ver 1.1 20150603
# 
# Kota Miura (miura@embl.de) http://cmci.embl.de
#
# License: GPLv3 (https://www.gnu.org/copyleft/gpl.html)

from fiji.threshold import Auto_Local_Threshold as ALT
from fiji.threshold import Auto_Threshold as AT
from ij.plugin.filter import ParticleAnalyzer as PA
from ij.plugin.filter import EDM, Binary
from ij import IJ, ImagePlus, Prefs
from ij.measure import ResultsTable
from ij.process import ImageConverter
import sys

Prefs.blackBackground = True

#### Settings to be changed depending on experiment#####
# number of dilate iteration
SAMPLEITER = 5
VERBOSE = False
#VERBOSE = True

#### -------------- #####

# load image into memory

#imp3 = ImagePlus('/Users/miura/Dropbox/people/Fukuda/cluster2.tif')
#imp3 = ImagePlus('/Users/miura/Dropbox/people/Fukuda/cluster.tif')
#imp3 = ImagePlus('/Users/miura/Dropbox/people/Fukuda/random.tif')
imp3 = IJ.getImage()
if imp3.getBitDepth() == 16:
   ImageConverter(imp3).convertToGray8()
elif imp3.getBitDepth() > 16:
   sys.exit()

# auto local threshold 
#thimp = ALT().exec(imp3, "Bernsen", 20, 0, 0, True)

#auto global threshold
hist = imp3.getProcessor().getHistogram()
lowTH = AT.Otsu(hist)
thimp = imp3.duplicate()
thimp.getProcessor().threshold(lowTH)

# fill holes
binner = Binary()
binner.setup("fill", None)
binner.run(thimp.getProcessor())
# morphological open
binner.setup("open", None)
binner.run(thimp.getProcessor())

# watershed to 
edm = EDM()
edm.setup("watershed", None)
#edm.run(thimp[0].getProcessor())
edm.run(thimp.getProcessor())
#thimp.show()
#binimp = thimp[0]
binimp = thimp
binorg = binimp.duplicate()
if VERBOSE:
	binorg.show()

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

	


