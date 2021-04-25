"""
This program is not intended to be included in the release of the program. It is being used to generate the pickle filer for
the message dictionary.
"""

import codecs
import pickle

list_o_people = ["Jacob Goldstein", "Daniel Morrison", "Nicole Lauch", "Lily Kull", "Briana Smith", "Morgan Huyler"]
list_o_people.sort()

AboutDict = {
    "1.00": ["Jonathan Shamberg", "September 30, 2021", "Jmshamberg@gmail.com", list_o_people]
}

sqlite3_keyword_masterlist = ["ABORT", "ACTION", "ADD", "AFTER", "ALL", "ALTER", "ALWAYS", "ANALYZE", "AND", "AS",
                              "ASC", "ATTACH", "AUTOINCREMENT", "BEFORE", "BEGIN", "BETWEEN", "BY", "CASCADE",
                              "CASE", "CAST", "CHECK", "COLLATE", "COLUMN", "COMMIT", "CONFLICT", "CONSTRAINT", "CREATE", "CROSS",
                              "CURRENT", "CURRENT_DATE", "CURRENT_TIME", "CURRENT_TIMESTAMP", "DATABASE", "DEFAULT", "DEFERRABLE",
                              "DEFERRED", "DELETE", "DESC", "DETACH", "DISTINCT", "DO", "DROP", "EACH", "ELSE", "END", "ESCAPE",
                              "EXCEPT", "EXCLUDE", "EXCLUSIVE", "EXISTS", "EXPLAIN", "FAIL", "FILTER", "FIRST", "FOLLOWING",
                              "FOR", "FOREIGN", "FROM", "FULL", "GENERATED", "GLOB", "GROUP", "GROUPS", "HAVING", "IF", "IGNORE",
                              "IMMEDIATE", "IN", "INDEX", "INDEXED", "INITIALLY", "INNER", "INSERT", "INSTEAD", "INTERSECT",
                              "INTO", "IS", "ISNULL", "JOIN", "KEY", "LAST", "LEFT", "LIKE", "LIMIT", "MATCH", "MATERIALIZED",
                              "NATURAL", "NO", "NOT", "NOTHING", "NOTNULL", "NULL", "NULLS", "OF", "OFFSET", "ON", "OR", "ORDER",
                              "OTHERS", "OUTER", "OVER", "PARTITION", "PLAN", "PRAGMA", "PRECEDING", "PRIMARY", "QUERY", "RAISE",
                              "RANGE", "RECURSIVE", "REFERENCES", "REGEXP", "REINDEX", "RELEASE", "RENAME", "REPLACE", "RESTRICT",
                              "RETURNING", "RIGHT", "ROLLBACK", "ROW", "ROWS", "SAVEPOINT", "SELECT", "SET", "TABLE", "TEMP", "TEMPORARY",
                              "THEN", "TIES", "TO", "TRANSACTION", "TRIGGER", "UNBOUNDED", "UNION", "UNIQUE", "UPDATE", "SING", "VACUUM",
                              "VALUES", "VIEW", "VIRTUAL", "WHEN", "WHERE", "WINDOW", "WITH", "WITHOUT"]


def welcome_messages():
    list_of_messages = [['message0.txt', 0, 'Welcome'], ['message1.txt', 1, 'Welcome Back' ]]
    MessageDict = {}

    for textFile in list_of_messages:
        with open(textFile[0], 'r') as message:
            message_list = message.readlines()
            message_text = ""
            for message_line in message_list:
                message_text += message_line
            MessageDict[textFile[1]] = [textFile[2], message_text]
    return MessageDict


if __name__ == "__main__":
    f = open("welcomedictionary.pkl", "wb")
    welcomeMessageDict = welcome_messages()
    pickle.dump(welcomeMessageDict, f)
    f.close()

    # f = codecs.open("version", "w", "utf-8-sig")
    # f.write("1.00")
    # f.close()
    #
    # f = open("../AboutInfo.pkl", "wb")
    # pickle.dump(AboutDict, f)
    # f.close()

    # f = open("../sql_Keyword_list.pkl", "wb")
    # pickle.dump(sqlite3_keyword_masterlist, f)
    # f.close()
