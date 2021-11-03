from orator.migrations import Migration


class CreatePagesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('pages') as table:
            table.increments('id')
            table.string('title', 1000)
            table.string('wikidata_id', 1000).nullable()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('pages')
