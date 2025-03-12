




from library.profile import data as jsondata





ifc = IfcBp().create("testproject","testlibrary")
ifc.organisation_application("3BM", "Jonathan")
ifc.ownerhistory()
ifc.site_building("Site","Building")

ifc.write("test.ifc")