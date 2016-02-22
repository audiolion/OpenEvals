from django.db import models

class EvalQuestions(models.Model):
    number = models.IntegerField(db_column='QUESTION_NUMBER')
    title = models.CharField(db_column='QUESTION_TITLE', max_length=100)
    text = models.CharField(db_column='QUESTION_TEXT', max_length=250)

    class Meta:
        managed = True
        db_table = 'CLASS_EVAL_QUESTIONS'

class EvalResults(models.Model):
    term_code = models.CharField(db_column='TERM_CODE', max_length=4)
    class_code = models.CharField(db_column='CLASS_CODE', max_length=30)
    class_desc = models.CharField(db_column='CLASS_DESC', max_length=100)
    instr_full_name = models.CharField(db_column='INSTR_FULL_NAME', max_length=100)
    instr_last_name = models.CharField(db_column='INSTR_LAST_NAME', max_length=50)
    instr_first_name = models.CharField(db_column='INSTR_FIRST_NAME', max_length=50)
    class_subj = models.CharField(db_column='CLASS_SUBJ',max_length=8)
    class_cat_nbr = models.CharField(db_column='CLASS_CAT_NBR', max_length=10)
    class_section = models.CharField(db_column='CLASS_SECTION', max_length=4)
    class_number = models.IntegerField(db_column='CLASS_NUMBER')
    q1_average = models.DecimalField(db_column='Q1_AVERAGE', max_digits=4, decimal_places=2)
    q2_average = models.DecimalField(db_column='Q2_AVERAGE', max_digits=4, decimal_places=2)
    q3_average = models.DecimalField(db_column='Q3_AVERAGE', max_digits=4, decimal_places=2)
    q4_average = models.DecimalField(db_column='Q4_AVERAGE', max_digits=4, decimal_places=2)
    q5_average = models.DecimalField(db_column='Q5_AVERAGE', max_digits=4, decimal_places=2)
    q6_average = models.DecimalField(db_column='Q6_AVERAGE', max_digits=4, decimal_places=2)
    q7_average = models.DecimalField(db_column='Q7_AVERAGE', max_digits=4, decimal_places=2)
    q8_average = models.DecimalField(db_column='Q8_AVERAGE', max_digits=4, decimal_places=2)
    q9_average = models.DecimalField(db_column='Q9_AVERAGE', max_digits=4, decimal_places=2)
    q10_average = models.DecimalField(db_column='Q10_AVERAGE', max_digits=4, decimal_places=2)
    campus = models.CharField(db_column='CAMPUS', max_length=5)

    class Meta:
        managed = True
        db_table = 'CLASS_EVAL_RESULTS'
