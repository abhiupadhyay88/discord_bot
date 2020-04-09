from googlesearch import search


class BotResult:
    """ Bot Result Engine to get command results
        Execute google search and get search result and store the history in database
        Get recent search done by users and return them for recent commands.
    """
    def __init__(self,command,username):
        self.command = command
        self.username = username

    def execute_command(self,query,bot_db):
        """function to execute command related to bot
        """
        if self.command == 'google':
            return self.search_google(query,bot_db)
        elif self.command == 'recent':
            return self.fetch_recent(query,bot_db)

    def search_google(self,query,bot_db):
        """Function to search google and return results
        """
        results = []
        try:
            bot_db.insert_history(self.username,query)
        except Exception as e:
            print(e)

        try:
            for i in search(query,tld='com',num=5,start=0,stop=5):
                results.append(i)
        except:
            pass
        return results

    def fetch_recent(self,query,bot_db):
        """function to return recent searches used made
        """
        try:
            db_results = bot_db.fetch_history(self.username, query)
        except Exception as e:
            print(e)
            db_results = []

        results = [res[2] for res in db_results]
        return results







