from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, SelectField
from wtforms.validators import Length


STATE_ABBR = [("AL", "Alabama"), ("AK", "Alaska"), ("AZ", "Arizona"), ("AR", "Arkansas"), ("CA", "California"), ("CO", "Colorado"), ("CT", "Connecticut"), ("DE", "Delaware"), ("FL", "Florida"), ("GA", "Georgia"), ("HI", "Hawaii"), ("ID", "Idaho"), ("IL", "Illinois"), ("IN", "Indiana"), ("IA", "Iowa"), ("KS", "Kansas"), ("KY", "Kentucky"), ("LA", "Louisiana"), ("ME", "Maine"), ("MD", "Maryland"), ("MA", "Massachusetts"), ("MI", "Michigan"), ("MN", "Minnesota"), ("MS", "Mississippi"), ("MO", "Missouri"), ("MT", "Montana"), ("NE", "Nebraska"), ("NV", "Nevada"), ("NH", "New Hampshire"), ("NJ", "New Jersey"), ("NM", "New Mexico"), ("NY", "New York"), ("NC", "North Carolina"), ("ND", "North Dakota"), ("OH", "Ohio"), ("OK", "Oklahoma"), ("OR", "Oregon"), ("PA", "Pennsylvania"), ("RI", "Rhode Island"), ("SC", "South Carolina"), ("SD", "South Dakota"), ("TN", "Tennessee"), ("TX", "Texas"), ("UT", "Utah"), ("VT", "Vermont"), ("VA", "Virginia"), ("WA", "Washington"), ("WV", "West Virginia"), ("WI", "Wisconsin"), ("WY", "Wyoming")]

# Declare Form Classes
# Form for the zipcode input on the temp_form template


class CurrentTempForm(FlaskForm):
    zipcode = StringField('Enter the Zip Code', validators=[Length(min=5, max=5, message="Valid US ZipCode is 5 digits")])
    submit = SubmitField('CHECK TEMPERATURE')

# Class for the zipcode input on the forcast_form template


class ForcastForm(FlaskForm):
    zipcode = StringField('Enter the Zip Code', validators=[Length(min=5, max=5, message="Valid US ZipCode is 5 digits")])
    submit = SubmitField('CHECK FORCAST')


class LookupForm(FlaskForm):
    cityName = StringField("City")
    stateName = SelectField(u'State', choices=STATE_ABBR)
    submit = SubmitField("Submit")
