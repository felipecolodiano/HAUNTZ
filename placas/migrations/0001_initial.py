# Generated by Django 2.2.4 on 2019-12-02 00:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cadastro_lote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Lote_numero', models.CharField(max_length=50, verbose_name='Numero do lote')),
                ('Ativo', models.BooleanField(default=True, verbose_name='Lote Ativo')),
            ],
            options={
                'db_table': 'CADASTRO_LOTE',
            },
        ),
        migrations.CreateModel(
            name='Cadastro_placas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Numero_serie', models.CharField(max_length=120, unique=True, verbose_name='Número de série')),
                ('Revisao_lm', models.IntegerField(verbose_name='Revisao LM')),
                ('Observacao', models.TextField(blank=True, verbose_name='Observação')),
                ('Ativo', models.BooleanField(default=True, verbose_name='Placa Ativa')),
            ],
            options={
                'db_table': 'CADASTRO_PLACAS',
            },
        ),
        migrations.CreateModel(
            name='Menu_placas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nome', models.CharField(max_length=120, verbose_name='Nome')),
                ('Caminho', models.CharField(max_length=199, unique=True, verbose_name='Caminho')),
            ],
            options={
                'db_table': 'MENU_PLACAS',
            },
        ),
        migrations.CreateModel(
            name='Modelo_placas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Modelo', models.CharField(max_length=120, verbose_name='modelo')),
                ('Descricao', models.CharField(max_length=200, verbose_name='Descrição')),
                ('Ativo', models.BooleanField(default=True, verbose_name='Modelo Ativo')),
            ],
            options={
                'db_table': 'MODELO_PLACAS',
            },
        ),
        migrations.AddConstraint(
            model_name='modelo_placas',
            constraint=models.UniqueConstraint(fields=('Modelo', 'Descricao'), name='Constraint_modelo'),
        ),
        migrations.AddField(
            model_name='cadastro_placas',
            name='Lote_numero',
            field=models.ForeignKey(limit_choices_to={'Ativo': True}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Lote_numero_lote', to='placas.Cadastro_lote'),
        ),
        migrations.AddField(
            model_name='cadastro_placas',
            name='Modelo',
            field=models.ForeignKey(limit_choices_to={'Ativo': True}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='modelo_placas_modelo', to='placas.Modelo_placas'),
        ),
        migrations.AddConstraint(
            model_name='cadastro_lote',
            constraint=models.UniqueConstraint(fields=('Lote_numero',), name='Constraint_lote'),
        ),
        migrations.AddConstraint(
            model_name='cadastro_placas',
            constraint=models.UniqueConstraint(fields=('Numero_serie',), name='Constraint_placas'),
        ),
    ]
