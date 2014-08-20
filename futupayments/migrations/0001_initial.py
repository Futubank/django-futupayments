# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Payment'
        db.create_table('futupayments_payment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('transaction_id', self.gf('django.db.models.fields.BigIntegerField')(db_index=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('order_id', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('message', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('meta', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('futupayments', ['Payment'])

        # Adding unique constraint on 'Payment', fields ['state', 'transaction_id']
        db.create_unique('futupayments_payment', ['state', 'transaction_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Payment', fields ['state', 'transaction_id']
        db.delete_unique('futupayments_payment', ['state', 'transaction_id'])

        # Deleting model 'Payment'
        db.delete_table('futupayments_payment')


    models = {
        'futupayments.payment': {
            'Meta': {'ordering': "('-creation_datetime',)", 'unique_together': "(('state', 'transaction_id'),)", 'object_name': 'Payment'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'creation_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'meta': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'order_id': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'transaction_id': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['futupayments']
