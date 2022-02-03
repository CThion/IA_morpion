# ==============================================================================
"""PENTE : implementation of the "Penté" board game for two players"""
# ==============================================================================
__author__  = "Gwendal Prat and Clément Thion"
__version__ = "0.0"
__date__    = "2021-12-01"
# ==============================================================================
from ezTK import *
# ==============================================================================
class ConfigWin(Win):
  """configuration window for the "Penté" game"""
  def __init__(self, dim=8, score=5, nameA='Player A', nameB='Player B'):
    """create and show the configuration window"""
    Win.__init__(self,title="ConfigWin", op=2, grow=True) #config window
    # --------------------------------------------------------------------------
    font2='Arial 20 bold'
    Label(self, text='CONFIGURATION', width=23, bg='Black', fg='White',
          font=font2)
    # --------------------------------------------------------------------------
    frame = Frame(self, fold = 2, flow='ES')
    #----
    Label(frame, text='Name of player A :', width=13, anchor='SW',
          grow=True)
    self.p1 = Entry(frame)
    #----
    Label(frame, text='Name of player B :', width=13, anchor='SW',
          grow=True)
    self.p2 = Entry(frame)
    #----
    Label(frame, text='Board Dimensions :', width=16, anchor='SW',
          grow=False)
    self.dim = Scale(frame, scale=(dim,16), flow='W',state=dim)
    #----
    Label(frame, text='Score for Victory :', width=16, anchor='SW',
          grow=False)
    self.score = Scale(frame, scale=(score,15), flow='W', state=score)
    # --------------------------------------------------------------------------
    board = GameWin(self)
    Button(frame,text='START',command= board.show(), bg='Black', fg='White',
           font=font2)
    # --------------------------------------------------------------------------
    self.loop()
# ==============================================================================
class GameWin(Win):
  """game window for the "Penté" game"""
  def __init__(self, config):
    """create and show the game window, according to config parameters"""
    #- GETTING CONFIG SETTINGS ----
    self.NameA = ConfigWin.p1.state; self.NameB=ConfigWin.p2.state
    self.dim = ConfigWin.dim.state; self.score=ConfigWin.score.state
    # --------------------------------------------------------------------------
    Win.__init__(self,title="Pente", op=2,grow=True) #game window
    # --------
    self.cwin.A = Label(self, font=font2, height=1, border=2,
        text = (f'{self.NameA}'))
    
    self.cwin.A = Label(self, font=font2, height=1, border=2,
        text = (f'{self.NameB}'))
    # --------------------------------------------------------------------------
    self.cwin.exit()
    # self.game = Game(dim) # create kernel class and store it as attribute
  # ----------------------------------------------------------------------------
  def on_click(self, widget, code, mods):
    """callback function for all mouse click events"""
  # ----------------------------------------------------------------------------
  def show(self):
    """show current game board by setting state defined for each grid cell"""
  # ----------------------------------------------------------------------------
  def victory(self):
    """play victory animation"""
# ==============================================================================
class Game(object):
  """kernel class for the "Penté" game"""
  def __init__(self, dim=8):
    """create and initialize the grid data structure"""
  # ----------------------------------------------------------------------------
  def __call__(self, row, col, state=None):
    """get or set state for provided grid cell"""
  # ----------------------------------------------------------------------------
  def switch(self, row, col, valid=True):
    """switch valid/invalid state for neighborhood of provided grid cell"""
  # ----------------------------------------------------------------------------
  def align(self, row, col, player):
    """check if provided move creates align config and return score update"""
    # return 5 points for each detected align pattern
  # ----------------------------------------------------------------------------
  def capture(self, row, col, player):
    """check if provided move creates capture config and return score update"""
    # return 1 point for each detected capture pattern
# ==============================================================================
if __name__ == "__main__":
  ConfigWin()
# ==============================================================================
