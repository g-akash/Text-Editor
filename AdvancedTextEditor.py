#!/usr/bin/python

import wx
import wx.lib.dialogs
import wx.stc as stc
import keyword
import os 
from xml.dom.minidom import parse
import xml.dom.minidom

if wx.Platform == '__WXMSW__':
	faces ={
		'times' : 'Times New Roman',
		'mono' : 'Courier New',
		'helv' : 'Arial',
		'other' : 'Comic Sans MS',
		'size' : 10,
		'size2' : 8,
		}
elif wx.Platform == '__WXMAC__':
	faces ={
		'times' : 'Times New Roman',
		'mono' : 'Manoco',
		'helv' : 'Arial',
		'other' : 'Comic Sans MS',
		'size' : 12,
		'size2' : 10,
		}
else:
	faces ={
		'times' : 'Times',
		'mono' : 'Courier New',
		'helv' : 'Arial',
		'other' : 'Comic Sans MS',
		'size' : 12,
		'size2' : 10,
		}

class MainWindow(wx.Frame):
	def __init__(self, parent, title):
		self.dirname = ''
		self.filename = ''
		self.normalStylesFore = dict()
		self.normalStylesBack = dict()
		self.pythonStylesFore = dict()
		self.pythonStylesBack = dict()

		#editor options
		self.foldSymbols = 2
		self.leftMarginWidth = 25
		self.lineNumbersEnabled = True

		#initialize the application frame and create the styled text control
		wx.Frame.__init__(self,parent,title=title,size=(800,600))
		self.control = stc.StyledTextCtrl(self, style=wx.TE_MULTILINE | wx.TE_WORDWRAP)

		#make the zoomin and zoomout shortcuts
		self.control.CmdKeyAssign(ord('='),stc.STC_SCMOD_CTRL,stc.STC_CMD_ZOOMIN) #ctrl + = zoom in
		self.control.CmdKeyAssign(ord('-'),stc.STC_SCMOD_CTRL,stc.STC_CMD_ZOOMOUT) #ctrl + = zoom in

		#set python keywords for syntax highlightings
		self.control.SetLexer(stc.STC_LEX_PYTHON)
		self.control.SetKeyWords(0," ".join(keyword.kwlist))

		#set some properties from text control
		self.control.SetViewWhiteSpace(False)
		self.control.SetProperty("fold", "1")
		self.control.SetProperty("tab.timmy.whinge.level", "1")


		self.control.SetMargins(5,0)
		self.control.SetMarginType(1,stc.STC_MARGIN_NUMBER)
		self.control.SetMarginWidth(1, self.leftMarginWidth)

		#set foldsymbols style based on based on instance variable self.foldsymbolstyle

		if self.foldSymbols==0:
			#arrow pointing right for contracted symbols and arrow pointing down for expanded
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, 		stc.STC_MARK_ARROWDOWN, "black", "black")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDER, 			stc.STC_MARK_ARROW, 	"black","black")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, 		stc.STC_MARK_EMPTY,		"black","black")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, 		stc.STC_MARK_EMPTY,		"black","black")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, 		stc.STC_MARK_EMPTY, 	"white", "black")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, 	stc.STC_MARK_EMPTY,		"white","black")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIN, 	stc.STC_MARK_EMPTY, 	"white", "black")

		elif self.foldSymbols == 1:
			#plus for contracted folder and minus for expanded
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, 		stc.STC_MARK_MINUS, 	"white", "black")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDER, 			stc.STC_MARK_PLUS, 		"white","black")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, 		stc.STC_MARK_EMPTY,		"white","black")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, 		stc.STC_MARK_EMPTY,		"white","black")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, 		stc.STC_MARK_EMPTY, 	"white", "black")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, 	stc.STC_MARK_EMPTY,		"white","black")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIN, 	stc.STC_MARK_EMPTY, 	"white", "black")
		elif self.foldSymbols == 2:
			#use circular headers and curved joins
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, 		stc.STC_MARK_CIRCLEMINUS, 					"white", "#404040")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDER, 			stc.STC_MARK_CIRCLEPLUS, 					"white", "#404040")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, 		stc.STC_MARK_VLINE,							"white", "#404040")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, 		stc.STC_MARK_LCORNERCURVE,					"white", "#404040")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, 		stc.STC_MARK_CIRCLEPLUSCONNECTED, 			"white", "#404040")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, 	stc.STC_MARK_CIRCLEMINUSCONNECTED,			"white", "#404040")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, 	stc.STC_MARK_TCORNERCURVE,		 			"white", "#404040")
		elif self.foldSymbols == 3:
			#arrow pointing right for contracted symbols and arrow pointing down for expanded
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, 		stc.STC_MARK_BOXMINUX, 					"white", "#808080")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDER, 			stc.STC_MARK_BOXPLUS, 					"white", "#808080")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, 		stc.STC_MARK_VLINE,						"white", "#808080")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, 		stc.STC_MARK_LCORNER,					"white", "#808080")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, 		stc.STC_MARK_BOXPLUSCONNECTED, 			"white", "#808080")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, 	stc.STC_MARK_BOXMINUXCONNECTED,			"white", "#808080")
			self.control.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIN, 	stc.STC_MARK_TCORNER, 					"white", "#808080")



		#status bar at the bottom
		self.CreateStatusBar()
		self.StatusBar.SetBackgroundColour((220,220,220))

		#file menu
		filemenu = wx.Menu()
		menuNew = filemenu.Append(wx.ID_NEW,"&New", "Create a new Document")
		menuOpen = filemenu.Append(wx.ID_OPEN, "&Open", "Open an existing document")
		menuSave = filemenu.Append(wx.ID_SAVE,"&Save", "Save the current document")
		menuSaveAs = filemenu.Append(wx.ID_SAVEAS,"Save &As", "Save a new document")
		#menuSaveAss = filemenu.Append(wx.ID_EXIT,"Save &As", "Save a new document")
		filemenu.AppendSeparator()
		menuClose = filemenu.Append(wx.ID_ANY, "&Close", "Close the Application")


		#edit menu
		editmenu = wx.Menu()
		menuUndo = editmenu.Append(wx.ID_UNDO, "&Undo", " Undo last action")
		menuRedo = editmenu.Append(wx.ID_REDO, "&Redo", "Redo last action")
		editmenu.AppendSeparator()
		menuSelectAll = editmenu.Append(wx.ID_SELECTALL, "&Select All", "Select the entire document")
		menuCopy = editmenu.Append(wx.ID_COPY,"&Copy", "Copy the selected text")
		menuCut = editmenu.Append(wx.ID_CUT, "C&ut", "Cut the selected text")
		menuPaste = editmenu.Append(wx.ID_PASTE,"&Paste","Paste text from clipboard")


		#setting preferences menu
		prefmenu = wx.Menu()
		menuLineNumbers = prefmenu.Append(wx.ID_ANY, "Toggle &Line Numbers", "Show/Hide line numbers column" )
		
		#set up help menu
		helpmenu = wx.Menu()
		menuHowTo = helpmenu.Append(wx.ID_ANY, "&How to...", "Get the help using editor")
		helpmenu.AppendSeparator()
		menuAbout = helpmenu.Append(wx.ID_ANY, "&About", "Read about the editor and its making" )


		#create the menu bar
		menuBar = wx.MenuBar()

		menuBar.Append(filemenu,"&File")
		menuBar.Append(editmenu,"&Edit")
		menuBar.Append(prefmenu,"&Preferences")
		menuBar.Append(helpmenu,"&Help")
		self.SetMenuBar(menuBar)

		#Start new code here

		#file events
		self.Bind(wx.EVT_MENU,self.OnNew,menuNew)
		self.Bind(wx.EVT_MENU,self.OnOpen,menuOpen)
		self.Bind(wx.EVT_MENU,self.OnSave,menuSave)
		self.Bind(wx.EVT_MENU,self.OnSaveAs,menuSaveAs)
		self.Bind(wx.EVT_MENU,self.OnClose,menuClose)

		#edit events
		self.Bind(wx.EVT_MENU,self.OnUndo,menuUndo)
		self.Bind(wx.EVT_MENU,self.OnRedo,menuRedo)
		self.Bind(wx.EVT_MENU,self.OnSelectAll,menuSelectAll)
		self.Bind(wx.EVT_MENU,self.OnCopy,menuCopy)
		self.Bind(wx.EVT_MENU,self.OnCut,menuCut)
		self.Bind(wx.EVT_MENU,self.OnPaste,menuPaste)


		#preferences  events
		self.Bind(wx.EVT_MENU,self.OnToggleLineNumber,menuLineNumbers)
		
		#help events
		self.Bind(wx.EVT_MENU,self.OnHowTo,menuHowTo)
		self.Bind(wx.EVT_MENU,self.OnAbout,menuAbout)

		self.control.Bind(wx.EVT_KEY_UP, self.UpdateLineCol)
		self.control.Bind(wx.EVT_CHAR, self.OnCharEvent)

		#display the application
		self.Show()

		#defaulting the style
		self.control.StyleSetSpec(stc.STC_STYLE_DEFAULT,"face:%(helv)s,size:%(size)d"%faces)
		self.control.StyleClearAll()

		# global default styles for all languages
		self.control.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:%(helv)s,size:%(size)d" % faces)
		self.control.StyleSetSpec(stc.STC_STYLE_LINENUMBER, "back:#C0C0C0,face:%(helv)s,size:%(size2)d" % faces)
		self.control.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "face:%(other)s" % faces)
		self.control.StyleSetSpec(stc.STC_STYLE_BRACELIGHT, "fore:#FFFFFF,back:#0000FF,bold")
		self.control.StyleSetSpec(stc.STC_STYLE_BRACEBAD, "fore:#000000,back:#FF0000,bold")

		#set all the theme settings
		self.ParseSettings("settings.xml")
		self.SetStyling()

	#setting the styles

	def SetStyling(self):
		#set the general foreground and background styles for python and normal styles
		pSFore = self.pythonStylesFore
		pSBack = self.pythonStylesBack
		nSFore = self.normalStylesFore
		nSBack = self.normalStylesBack
		print nSBack
		#python styles
		print nSBack
		self.control.StyleSetBackground(stc.STC_STYLE_DEFAULT, nSBack["Main"])
		self.control.SetSelBackground(True , "#333333")

		#default
		self.control.StyleSetSpec(stc.STC_P_DEFAULT, "fore:%s,back:%s" % (pSFore["Default"], pSBack["Default"]))
		self.control.StyleSetSpec(stc.STC_P_DEFAULT, "face:%(helv)s,size:%(size)d" % faces)

		# Comments
		self.control.StyleSetSpec(stc.STC_P_COMMENTLINE, "fore:%s,back:%s" % (pSFore["Comment"], pSBack["Comment"]))
		self.control.StyleSetSpec(stc.STC_P_COMMENTLINE, "face:%(other)s,size:%(size)d" % faces)

		# Number
		self.control.StyleSetSpec(stc.STC_P_NUMBER, "fore:%s,back:%s" % (pSFore["Number"], pSBack["Number"]))
		self.control.StyleSetSpec(stc.STC_P_NUMBER, "size:%(size)d" % faces)

		# String
		self.control.StyleSetSpec(stc.STC_P_STRING, "fore:%s,back:%s" % (pSFore["String"], pSBack["Number"]))
		self.control.StyleSetSpec(stc.STC_P_STRING, "face:%(helv)s,size:%(size)d" % faces)

		# Single-quoted string
		self.control.StyleSetSpec(stc.STC_P_CHARACTER, "fore:%s,back:%s" % (pSFore["SingleQuoteString"], pSBack["SingleQuoteString"]))
		self.control.StyleSetSpec(stc.STC_P_CHARACTER, "face:%(helv)s,size:%(size)d" % faces)

		# Keyword
		self.control.StyleSetSpec(stc.STC_P_WORD, "fore:%s,back:%s" % (pSFore["Keyword"], pSBack["Keyword"]))
		self.control.StyleSetSpec(stc.STC_P_WORD, "bold,size:%(size)d" % faces)

		# Triple quotes
		self.control.StyleSetSpec(stc.STC_P_TRIPLE, "fore:%s,back:%s" % (pSFore["TripleQuote"], pSBack["TripleQuote"]))
		self.control.StyleSetSpec(stc.STC_P_TRIPLE, "size:%(size)d" % faces)

		# Triple double quotes
		self.control.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "fore:%s,back:%s" % (pSFore["TripleDoubleQuote"], pSBack["TripleDoubleQuote"]))
		self.control.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "size:%(size)d" % faces)

		# Class name definition
		self.control.StyleSetSpec(stc.STC_P_CLASSNAME, "fore:%s,back:%s" % (pSFore["ClassName"], pSBack["ClassName"]))
		self.control.StyleSetSpec(stc.STC_P_CLASSNAME, "bold,underline,size:%(size)d" % faces)

		# Function name definition
		self.control.StyleSetSpec(stc.STC_P_DEFNAME, "fore:%s,back:%s" % (pSFore["FunctionName"], pSBack["FunctionName"]))
		self.control.StyleSetSpec(stc.STC_P_DEFNAME, "bold,size:%(size)d" % faces)

		# Operators
		self.control.StyleSetSpec(stc.STC_P_OPERATOR, "fore:%s,back:%s" % (pSFore["Operator"], pSBack["Operator"]))
		self.control.StyleSetSpec(stc.STC_P_OPERATOR, "bold,size:%(size)d" % faces)

		# Identifiers
		self.control.StyleSetSpec(stc.STC_P_IDENTIFIER, "fore:%s,back:%s" % (pSFore["Identifier"], pSBack["Identifier"]))
		self.control.StyleSetSpec(stc.STC_P_IDENTIFIER, "face:%(helv)s,size:%(size)d" % faces)

		# Comment blocks
		self.control.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "fore:%s,back:%s" % (pSFore["CommentBlock"], pSBack["CommentBlock"]))
		self.control.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "size:%(size)d" % faces)

		# End of line where string is not closed
		self.control.StyleSetSpec(stc.STC_P_STRINGEOL, "fore:%s,back:%s" % (pSFore["StringEOL"], pSBack["StringEOL"]))
		self.control.StyleSetSpec(stc.STC_P_STRINGEOL, "face:%(mono)s,eol,size:%(size)d" % faces)

		# Caret/Insertion Point
		self.control.SetCaretForeground(pSFore["Caret"])
		self.control.SetCaretLineBackground(pSBack["CaretLine"])
		self.control.SetCaretLineVisible(True)




	def OnNew(self, e):
		self.filename = ''
		self.control.SetValue('')

	def OnOpen(self, e):
		try:
			dlg = wx.FileDialog(self, "Choose a file",self.dirname,"","*.*",wx.FD_OPEN)
			if(dlg.ShowModal()== wx.ID_OK):
				self.filename = dlg.GetFilename()
				self.dirname = dlg.GetDirectory()
				f = open(os.path.join(self.dirname,self.filename),'r')
				self.control.SetValue(f.read())
				f.close()
			dlg.Destroy()
		except:
			dlg = wx.MessageDialog(self,"Couldn't open file","Error",wx.ICON_ERROR)
			dlg.ShowModal()
			dlg.Destroy()

	def OnSave(self,e):
		try:
			f=open(os.path.join(self.dirname,self.filename),'w')
			f.write(self.control.GetValue())
			f.close()
		except:
			try:
				dlg = wx.FileDialog(self,"Save file as",self.dirname,"Untitled","*.*",wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
				if(dlg.ShowModal()==wx.ID_OK):
					self.filename = dlg.GetFilename()
					self.dirname = dlg.GetDirectory()
					f=open(os.path.join(self.dirname,self.filename),'w')
					f.write(self.control.GetValue())
					f.close()
				dlg.Destroy()
			except:
				pass

	def OnSaveAs(self,e):
		try:
			dlg = wx.FileDialog(self,"Save file as",self.dirname,"Untitled","*.*",wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
			if(dlg.ShowModal()==wx.ID_OK):
				self.filename = dlg.GetFilename()
				self.dirname = dlg.GetDirectory()
				f=open(os.path.join(self.dirname,self.filename),'w')
				f.write(self.control.GetValue())
				f.close()
			dlg.Destroy()
		except:
			pass

	def OnClose(self,e):
		self.Close(True)

	def OnUndo(self,e):
		self.control.Undo()

	def OnRedo(self,e):
		self.control.Redo()

	def OnSelectAll(self,e):
		self.control.SelectAll()

	def OnCopy(self,e):
		self.control.Copy()

	def OnCut(self,e):
		self.control.Cut()

	def OnPaste(self,e):
		self.control.Paste()

	def OnToggleLineNumber(self,e):
		if self.lineNumbersEnabled == True:
			self.control.SetMarginWidth(1,0)
			self.lineNumbersEnabled = False
		else:
			self.control.SetMarginWidth(1,self.leftMarginWidth)
			self.lineNumbersEnabled = True

	def OnHowTo(self,e):
		dlg = wx.lib.dialogs.ScrolledMessageDialog(self,"This is how to", "How to", size=(400,400))
		dlg.ShowModal()
		dlg.Destroy()

	def OnAbout(self,e):
		dlg = wx.MessageDialog(self,"My advanced text editor I made with wx and python", "About", wx.OK)
		dlg.ShowModal()
		dlg.Destroy()

	def UpdateLineCol(self,e):
		line = self.control.GetCurrentLine()+1
		col = self.control.GetColumn(self.control.GetCurrentPos())
		stat = "Line %s, Column %s"%(line,col)
		self.StatusBar.SetStatusText(stat,0)


	#left mouse up
	def OnLeftUp(self, e):
		#if we click a position in the text box it will update line and col accordingly
		self.UpdateLineCol(self)
		e.skip()



	def OnCharEvent(self,e):
		keycode = e.GetKeyCode()
		altDown = e.AltDown()
		if(keycode==14): #Ctrl + N
			self.OnNew(self)
		elif(keycode==15): #Ctrl + O
			self.OnOpen(self)
		elif(keycode==19): #Ctrl + S
			self.OnSave(self)
		elif(altDown and (keycode==223)): #Alt +S 
			self.OnSaveAs(self)
		elif(keycode==23):	#Ctrl + W
			self.OnClose(self)
		elif(keycode==340):	#F1
			self.OnHowTo (self)
		elif(keycode==341):	#F2
			self.OnAbout(self)
		else:
			e.Skip()
			#pass


	#update the user interface
	def OnUpdateUI(self, e):
		braceAtCaret = -1
		braceOpposite = -1
		charBefore = None
		caretPos = self.controlGetPos()

		if (caretPos >0):
			charBefore = self.control.GetCharAt(caret-1)
			styleBefore = self.control.GetStyleAt(caret-1)

		#check before
		if(charBefore and chr(charBefore) in "(){}[]" and styleBefore == stc.STC_P_OPERATOR):
			braceAtCaret = caretPos -1 

		#check after
		if(braceAtCaret<1):
			charAfter = self.control.GetCharAt(caretPos)
			styleAfter = self.control.GetStyleAt(caretPos)

			if(charAfter and chr(charAfter) in "{}[]()" and styleAfter == self.STC_P_OPERATOR):
				braceAtCaret = caretPos


		if(braceAtCaret>=0):
			braceOpposite = self.control.BraceMatch(braceAtCaret)

		if (braceAtCaret != -1 and braceOpposite == -1):
			self.control.BraceBadLight(braceAtCaret)
		else:
			self.control.BraceHighlight(braceAtCaret,braceOpposite) 

	#handles the clicking on margin
	def OnMarginClick(self, e):
		#fold and unfold whenever needed
		if(e.GetMargin == 2):
			if(e.GetShift() and e.GetControl()):
				self.Control.FoldAll()

			else:
				lineClicked = self.control.LineFromPosition(e.GetPosition())

				if(self.control.GetFoldLevel(lineClicked) & stc.STC_P_FOLDLEVELHEADERFLAG):
					if(e.GetShift()):
						self.control.SetFoldExpanded(lineClicked, True)
						self.control.Expand(lineClicked, True, True, -1)

					elif(e.GetControl()):
						if(self.control.GetFoldExpanded(lineClicked)):
							self.control.SetFoldExpanded(lineClicked, False)
							self.control.Expand(lineClicked, False, False, 0)
						else:
							self.control.SetFoldExpanded(lineClicked, True)
							self.control.Expand(lineClicked, True, True, 100)
					else:
						self.control.ToggleFold(lineClicked)

	#Folds all the blocks of code
	def FoldAll(self):
		lineCount = self.control.GetLineCount()
		expanding = True

		#check if we are folding or unfolding
		for linenum in range(lineCount):
			if self.GetFoldLevel(linenum) & stc.STC_FOLDERLEVELHEADERFLAG:
				expanding = not self.GetFoldLevel(linenum)
				break

		linenum = 0

		while linenum < lineCount:
			level = self.GetFoldLevel(linenum)
			if level & stc.STC_FOLDERHEADERFLAG and \
				(level & stc.STC_FOLDERLEVELNUMBERMASK== stc.STC_FOLDERLEVELBASE):

				if expanding:
					self.SetFoldExpanded(linenum, True)
					linenum = self.Expand(linenum, True)
					linenum = linenum-1
				else:
					lastchild = self.GetLastChild(linenum-1)
					self.SetFoldExpanded(linenum, False)

					if lastchild > linenum:
						self.HideLines(linenum+1, lastchild)

		linenum = linenum+1


	def Expand(self, line, doExpand, force = False, visLevels=0, level = -1):
		lastChild = self.GetLastChild(line, level)
		line = line + 1

		while line <= lastChild:
			if force:
				if visLevels>0:
					self.ShowLines(line,line)
				else:
					self.HideLines(line,line)
			else:
				if doExpand:
					self.ShowLines(line,line)

			if level == -1:
				level = self.GetFoldLevel(line)

			if level & stc.STC_FOLDLEVELHEADERFLAG:
				if fold:
					if visLevels>1:
						self.SetFoldExpanded(line, True)
					else:
						self.SetFoldExpanded(line, False)

					line = self.Expand(line, doExpand, force, visLevels-1)

				else:
					if doExpand and self.GetFoldExpanded(line):
						line = self.Expand(line, True, force, visLevels-1)
					else:
						line = self.Expand(line, False, force, visLevels-1)


			else:
				line = line + 1

		return line

	#key press event bindings

	def OnKeyPressed(self, e):
		#if the tip is already up hide it
		if(self.control.CallTipActive()):
			self.control.CallTipCancel()
		key = e.GetKeyCode()

		#ctrl + space for autocomplete
		if key == 32 and e.ControlDown():
			pos = self.control.GetCurrentPos()

			#small tool tip box
			if e.ShiftDown():
				self.control.CallTipSetBackground("yellow")
				self.control.CallTipShow(pos,"Press <ctrl> + <space> for code completion")
			else:
				kw = keyword.kwlist[:]
				kw.sort()
				self.control.AutoCompleteIgnoreCase(False)
				self.control.AutoCompShow(0," ".join(kw))
		else:
			e.skip()

	#parses an xml file for all the styling and colors

	def ParseSettings(self, settings_file):
		#Open xml using minidon parser
		DOMTree = xml.dom.minidom.parse(settings_file)
		collection = DOMTree.documentElement

		#get all the styles in the collection
		styles = collection.getElementsByTagName("style")

		for s in styles:
			item = s.getElementsByTagName("item")[0].childNodes[0].data
			color = s.getElementsByTagName("color")[0].childNodes[0].data
			side = s.getElementsByTagName("side")[0].childNodes[0].data
			sType = s.getAttribute("type")

			if sType=="normal":
				if side == "Back":
					self.normalStylesBack[str(item)] = str(color)
				else:
					self.normalStylesFore[str(item)] = str(color)
			else:
				if side == "Back":
					self.pythonStylesBack[str(item)] = str(color)
				else:
					self.pythonStylesFore[str(item)] = str(color)



				








app = wx.App()
frame = MainWindow(None,"My Text Editor")
app.MainLoop()