# Generated from simba.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .simbaParser import simbaParser
else:
    from simbaParser import simbaParser

# This class defines a complete listener for a parse tree produced by simbaParser.
class simbaListener(ParseTreeListener):

    # Enter a parse tree produced by simbaParser#start.
    def enterStart(self, ctx:simbaParser.StartContext):
        pass

    # Exit a parse tree produced by simbaParser#start.
    def exitStart(self, ctx:simbaParser.StartContext):
        pass


    # Enter a parse tree produced by simbaParser#form.
    def enterForm(self, ctx:simbaParser.FormContext):
        pass

    # Exit a parse tree produced by simbaParser#form.
    def exitForm(self, ctx:simbaParser.FormContext):
        pass


    # Enter a parse tree produced by simbaParser#sequence.
    def enterSequence(self, ctx:simbaParser.SequenceContext):
        pass

    # Exit a parse tree produced by simbaParser#sequence.
    def exitSequence(self, ctx:simbaParser.SequenceContext):
        pass


    # Enter a parse tree produced by simbaParser#association.
    def enterAssociation(self, ctx:simbaParser.AssociationContext):
        pass

    # Exit a parse tree produced by simbaParser#association.
    def exitAssociation(self, ctx:simbaParser.AssociationContext):
        pass


    # Enter a parse tree produced by simbaParser#comment.
    def enterComment(self, ctx:simbaParser.CommentContext):
        pass

    # Exit a parse tree produced by simbaParser#comment.
    def exitComment(self, ctx:simbaParser.CommentContext):
        pass



del simbaParser