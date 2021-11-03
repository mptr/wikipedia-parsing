from orator.migrations import Migration


class CreateAmbiguitiesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('ambiguities') as table:
            table.increments('id')
            table.string('base', 1000)
            table.string('alt', 1000)
            table.enum('kind', [
                'link',
                'redirect',
                'spacy'
            ])
            table.integer('page_id').nullable()
            table.foreign('page_id').references('id').on('pages').on_delete('cascade')

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('ambiguities')
