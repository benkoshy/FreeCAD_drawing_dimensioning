
from dimensioning import *
import selectionOverlay 
import textAddDialog
from textSvg import SvgTextParser

d = DimensioningProcessTracker()

def EditDimensionText( event, referer, elementXML, elementParms, elementViewObject ):
    d.dimToEdit = elementViewObject    
    d.elementXML = elementXML
    selectionOverlay.hideSelectionGraphicsItems()
    e = elementXML
    debugPrint(3, e.XML[e.pStart:e.pEnd] )
    svgText = SvgTextParser( e.XML[e.pStart:e.pEnd] )
    d.svgText = svgText
    debugPrint(3, u'editing %s' % unicode(svgText))
    widgets = dict( [c.objectName(), c] for c in dialog.children() )
    widgets['textLineEdit'].setText( svgText.text )
    widgets['sizeLineEdit'].setText( svgText.font_size)
    widgets['colorLineEdit'].setText( svgText.fill )
    widgets['familyLineEdit'].setText( svgText.font_family )
    widgets['doubleSpinBox_rotation'].setValue(svgText.rotation)
    widgets['placeButton'].setText('Change')
    dialog.setWindowTitle('Editing %s' % elementViewObject.Name)
    dialog.show()
    
class EditTextDialogWidget( QtGui.QWidget ):
    def accept( self ):
        debugPrint(3, 'EditTextDialogWidget accept pressed')
        widgets = dict( [c.objectName(), c] for c in self.children() )
        debugPrint(4, 'widgets %s' % widgets)
        if widgets['textLineEdit'].text() == '':
            debugPrint(1, 'Aborting placing empty text.')
            return
        self.hide()
        svgText = d.svgText 
        svgText.text = widgets['textLineEdit'].text()
        widgets['textLineEdit'].setText('')
        svgText.font_size = widgets['sizeLineEdit'].text()
        svgText.font_family = widgets['familyLineEdit'].text()
        svgText.fill = widgets['colorLineEdit'].text()
        svgText.rotation =  widgets['doubleSpinBox_rotation'].value()
        debugPrint(3,'updating XML in %s to' % d.dimToEdit.Name)
        xml = svgText.toXML()
        debugPrint(4,xml)
        e =  d.elementXML
        newXML = e.XML[:e.pStart] + xml + e.XML[e.pEnd:]
        debugPrint(3,newXML)
        d.dimToEdit.ViewResult = newXML
        recomputeWithOutViewReset(d.drawingVars)
        

dialog = EditTextDialogWidget()
dialogUi = textAddDialog.Ui_Dialog()
dialogUi.setupUi(dialog)

maskBrush  =   QtGui.QBrush( QtGui.QColor(0,160,0,100) )
maskPen =      QtGui.QPen( QtGui.QColor(0,160,0,100) )
maskPen.setWidth(0.0)
maskHoverPen = QtGui.QPen( QtGui.QColor(0,255,0,255) )
maskHoverPen.setWidth(0.0)

class EditText:
    def Activated(self):
        V = getDrawingPageGUIVars()
        d.activate( V )
        selectGraphicsItems = selectionOverlay.generateSelectionGraphicsItems( 
            [obj for obj in V.page.Group  if obj.Name.startswith('dim')], 
            EditDimensionText , 
            sceneToAddTo = V.graphicsScene, 
            transform = V.transform,
            doTextItems = True, 
            pointWid=2.0,
            maskPen=maskPen, 
            maskHoverPen=maskHoverPen, 
            maskBrush = maskBrush
            )
        
    def GetResources(self): 
        msg = "Edit a dimension's text"
        return {
            'Pixmap' : os.path.join( iconPath , 'textEdit.svg' ) , 
            'MenuText': msg, 
            'ToolTip': msg
            } 
FreeCADGui.addCommand('dd_editText', EditText())


