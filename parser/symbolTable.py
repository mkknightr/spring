
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
            print("ADD NEW ITEM")
            return "ok"
        
    def GetItem(self, id): 
        """
        get llvm item from key (C name) 
        """
        level = self.m_cur_level 
        while level > 0:
            if id in self.m_table[level]: 
                return self.m_table[level][id]
            level -= 1
        return None


    def InGlobalScope(self):
        """
        check whether it is in global scope 
        """
        return (len(self.m_table) == 1)
    
    def exist(self, id): 
        """
        check whether id exists in the symbol table 
        """
        level = self.m_cur_level 
        while level > 0:
            if id in self.m_table[level]: 
                return True
            level -= 1
        return False 

    def display(self): 
        """
        print to debug 
        """
        print(self.m_table)