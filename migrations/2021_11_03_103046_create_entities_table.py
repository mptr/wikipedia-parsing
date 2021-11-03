from orator.migrations import Migration


class CreateEntitiesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('entities') as table:
            table.big_increments('id')
            table.integer('start')
            table.integer('end')
            table.string('content', 1000)
            table.enum('kind', [
                'CARDINAL',
                'DATE',
                'EVENT',
                'FAC',
                'GPE',
                'LANGUAGE',
                'LAW',
                'LOC',
                'MONEY',
                'NORP',
                'ORDINAL',
                'ORG',
                'PERCENT',
                'PERSON',
                'PRODUCT',
                'QUANTITY',
                'TIME',
                'WORK_OF_ART'
            ])
            table.integer('sentence_id')
            table.foreign('sentence_id').references('id').on('sentences').on_delete('cascade')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('entities')
