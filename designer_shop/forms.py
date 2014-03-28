from django import forms

from oscar.core.loading import get_model

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, Fieldset, HTML

SIZE_TYPES = [
    ('1', "Set (eg. Small, Medium, Large)"),
    ('2', "Dimensions (eg. Length X Width)"),
    ('3', "Number (eg. Dress size)")
]

SIZE_TYPES_AND_EMPTY = [('0', '*Choose a size type*')] + SIZE_TYPES

class ProductCreationForm(forms.ModelForm):

    sizeVariation = forms.ChoiceField(label='Size type',
                                         choices=SIZE_TYPES_AND_EMPTY,
                                         initial='0')

    def __init__(self, *args, **kwargs):
        super(ProductCreationForm, self).__init__(*args, **kwargs)
        # password = forms.CharField(label='Password', widget=forms.PasswordInput)

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        # helper.form_class = 'form-horizontal'

        self.helper.layout = Layout(
            Div(
                Fieldset('General',
                         Field('title', placeholder='Title'),
                         Field('description', placeholder='Description'),
                         Field('product_class', placeholder='Product Class')
                         ),
                Fieldset('Sizes and Colors',
                         Field('sizeVariation', placeholder='Choose a variation'),
                         Div(
                             Div(
                                 Div(HTML("""<a class="accordion-toggle" href="#collapse1" data-toggle="collapse" data-parent="#accordion2">Expand</a>"""),
                                     css_class="accordion-heading"
                                    ),
                                 Div(
                                     Div(
                                         HTML("""<table class="table" id="sizegrid1">
                                                      <thead>
                                                            <tr>
                                                                <td><b>ID</b></td>
                                                                <td><b>Name</b></td>
                                                                <td><b>Description</b><b></b></td>
                                                                <td><b>Color</b></td>
                                                            </tr>
                                                        </thead>
                                                        <tbody>
                                                            <tr>
                                                                <td>1</td>
                                                                <td>Banana</td>
                                                                <td>Bright and bent</td>
                                                                <td>Yellow</td>
                                                            </tr>
                                                            <tr>
                                                                <td>2</td>
                                                                <td>Apple</td>
                                                                <td>Kind of round</td>
                                                                <td>Red</td>
                                                            </tr>
                                                            <tr>
                                                                <td>3</td>
                                                                <td>Orange</td>
                                                                <td>Round</td>
                                                                <td>Orange</td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                              """

                                             ),
                                         css_class="accordion-inner"
                                         ),
                                         css_class="accordion-body collapse in", css_id="collapse1"
                                     ),
                                 css_class="accordion-group"
                                ),
                             css_class="accordion", css_id="accordion2"
                             ),
                         ),
                Submit('productCreationForm', 'Create', css_class='tinvilleButton'),
                css_class="container"
            )

        )

    class Meta:
        model = get_model('catalogue', 'Product')
        # fields = ['title', 'description', 'product_class']

                                #             <div class="accordion" id="accordion3">
                                #                 <div class="accordion-group">
                                #                     <div class="accordion-heading"><a class="accordion-toggle" href="#collapse2" data-toggle="collapse" data-parent="#accordion3">Vegetable</a></div>
                                #                     <div class="accordion-body collapse" id="collapse2">
                                #                         <div class="accordion-inner">
                                #                             <table class="table" id="veggiegrid">
                                #                                 <thead>
                                #                                 <tr>
                                #                                     <td><b>ID</b></td>
                                #                                     <td><b>Name</b></td>
                                #                                     <td><b>Description</b><b></b></td>
                                #                                     <td><b>Color</b></td>
                                #                                 </tr>
                                #                                 </thead>
                                #                                 <tbody>
                                #                                 <tr>
                                #                                     <td>1</td>
                                #                                     <td>Pumpkin</td>
                                #                                     <td>Odd shaped</td>
                                #                                     <td>Orange</td>
                                #                                 </tr>
                                #                                 <tr>
                                #                                     <td>2</td>
                                #                                     <td>Celery</td>
                                #                                     <td>Narrow and thin</td>
                                #                                     <td>Green</td>
                                #                                 </tr>
                                #                                 </tbody>
                                #                             </table>
                                #                         </div>
                                #                     </div>
                                #                 </div>
                                #             </div>
                                #         </div>
                                #     </div>
                                # </div>