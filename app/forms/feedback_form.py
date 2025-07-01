from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired

class FeedbackForm(FlaskForm):
     turma = SelectField('Turma', validators=[DataRequired()])
     professor = SelectField('Professor', validators=[DataRequired()])
     dificuldade = SelectField('Dificuldade', choices=[('1', '1 - Muito Fácil'),
                                                        ('2', '2 - Fácil'), 
                                                        ('3', '3 - Moderado'),
                                                        ('4', '4 - Difícil'),
                                                        ('5', '5 - Muito Difícil')], validators=[DataRequired()])
     qualidade = IntegerField('Qualidade', validators=[DataRequired()])
     comentario = StringField('Comentário', validators=[DataRequired()])
     submit = SubmitField('Enviar')
     cancel = SubmitField('Cancelar')
     delete = SubmitField('Excluir')
     edit = SubmitField('Editar')
