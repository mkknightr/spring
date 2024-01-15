
class SymbolTable: 
    """
    symbol table
    """
    def __init__(self): 
        """
        set up the symbol table
        """
        self.m_table = [{}]
        self.m_cur_level = 0 

    def EnterScope(self): 
        """
        enter a scope
        """
        self.m_cur_level += 1 
        self.m_table.append({})
    def QuitScope(self): 
        """
        quit a scope 
        """
        if self.m_cur_level == 0: 
            return 
        self.m_table.pop(-1)
        self.m_cur_level -= 1


    def AddItem(self, key, value): 
        """
        add new items for symbol table
        """
        if key in self.m_table[self.m_cur_level]: 
            return f"redefinition of variable {key} " 
        else: 
            self.m_table[self.m_cur_level][key] = value
            return "ok"
    def display(self): 
        """
        print to debug 
        """
        print(self.m_table)