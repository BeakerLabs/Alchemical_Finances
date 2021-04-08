"""
This program is not intended to be included in the release of the program. It is being used to generate the pickle filer for
the message dictionary.
"""

import codecs
import pickle

welcomeMessageDict = {
    0: ["Welcome", "I am glad you have chosen to use my Finance Ledger to manage your personal finances. This project has been in the works for what feels like a decade. "
                   "The program you are using has evolved over the year from simple spreedsheet ledgers as my personal finances expanded and knowledge on the subject expanded."
                   "\n\nThe design of this project is based upon the core principal:\n\n'Everyones Personal Finances are Unique.'\n\nWhich explains .. why i should really write this later."],
    1: ["Welcome Back", """Another message I should really write at another time in the day"""]
}

AboutDict = {
    "1.00": ["Jonathan Shamberg", "September 30, 2021", "Jmshamberg@gmail.com", "I have much work do do in this regards"]
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


if __name__ == "__main__":
    # f = open("welcomedictionary.pkl", "wb")
    # pickle.dump(welcomeMessageDict, f)
    # f.close()
    #
    # f = codecs.open("version", "w", "utf-8-sig")
    # f.write("1.00")
    # f.close()
    #
    # f = open("../AboutInfo.pkl", "wb")
    # pickle.dump(AboutDict, f)
    # f.close()
    f = open("../sql_Keyword_list.pkl", "wb")
    pickle.dump(sqlite3_keyword_masterlist, f)
    f.close()
