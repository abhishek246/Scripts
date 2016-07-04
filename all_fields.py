'''
   This scripts generates all possible fields
   access able by the given base_model.

   Constraint: Fetchs fields only till depth of 2.
'''
__author__ = 'Abhishek K'
__credits__ = ['Farhan Ali', 'Jaydeep']

from django.db.models.fields.related import ForeignKey, ManyToOneRel, OneToOneRel, ManyToManyRel

def data(base_model, depth=0):
    model_coloums = base_model._meta.get_fields_with_model()
    column_names = list()
    try:
        for model in model_coloums:
            type_of_field = model[0]
            if isinstance(type_of_field, ForeignKey) and depth < 2:
                fk_column_names = data(type_of_field.__dict__.get('related_model'), depth + 1)
                prefix = type_of_field.__dict__.get('name')
                column_names += [prefix +'__' + col if col else '' for col in fk_column_names]
            elif isinstance(type_of_field, ManyToManyRel) and depth < 2:
                m2m_column_names = data(type_of_field.__dict__.get('related_model'), depth + 1)
                prefix = type_of_field.__dict__.get('related_name')
                if not prefix:
                    prefix = type_of_field.name+'_set'
                column_names += [prefix + '__' + col if col else '' for col in m2m_column_names]
            elif isinstance(type_of_field, ManyToOneRel) and depth < 2:
                if isinstance(type_of_field.__dict__.get('related_model'), base_model):
                    continue
                else:
                    m2one_column_names = data(type_of_field.__dict__.get('related_model'), depth + 1)
                    prefix = type_of_field.__dict__.get('related_name')
                    if not prefix:
                        prefix = type_of_field.name+'_set'
                    column_names += [prefix +'__' + col if col else '' for col in m2one_column_names]
            elif isinstance(type_of_field, OneToOneRel) and depth < 2:
                a = 1
            else:
                column_name = type_of_field.__dict__.get('column')
                column_names.append(str(column_name))
        return list(set(column_names))
    except Exception, e:
        error_log(e)

