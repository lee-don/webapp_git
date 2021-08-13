
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import Required, DataRequired
from wtforms.fields.html5 import DateField

class LoginForm(FlaskForm):
    acc = StringField('',
                      render_kw={
                          'class': 'un'
                      },
                      validators=[DataRequired()])

    password = PasswordField(
        render_kw={'class': 'pass'},
    )

    submit = SubmitField('登录',
                         render_kw={
                             'class': 'submit'
                         })


class DaylyForm(FlaskForm):
    acc = StringField('上报人',
                      render_kw={
                          'class': 'un'
                      },
                      validators=[DataRequired()])

    date = DateField('日期',
        render_kw={'class': 'un'},
    )

    tag = SelectField(
        label='类别',
        validators=[DataRequired('请选择标签')],
        render_kw={
            'class': 'un'
        },
        choices=[(1, '情感'), (2, '星座'), (3, '爱情')],
        default = 3,
        coerce=int
    )

    submit = SubmitField('提交',
                         render_kw={
                             'class': 'submit'
                         })





