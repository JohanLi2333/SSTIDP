from django.urls import path

from . import views

app_name = "dataset"
urlpatterns = [
    path("dataset", views.Dataset.as_view(), name="dataset"),
    path("dataset/web", views.Dataset.CreateWebDataset.as_view()),
    path("dataset/qa", views.Dataset.CreateQADataset.as_view()),
    path(
        "dataset/<str:dataset_id>", views.Dataset.Operate.as_view(), name="dataset_key"
    ),
    path(
        "dataset/<str:dataset_id>/export", views.Dataset.Export.as_view(), name="export"
    ),
    path(
        "dataset/<str:dataset_id>/export_zip",
        views.Dataset.ExportZip.as_view(),
        name="export_zip",
    ),
    path(
        "dataset/<str:dataset_id>/re_embedding",
        views.Dataset.Embedding.as_view(),
        name="dataset_key",
    ),
    path("dataset/<str:dataset_id>/application", views.Dataset.Application.as_view()),
    path(
        "dataset/<int:current_page>/<int:page_size>",
        views.Dataset.Page.as_view(),
        name="dataset",
    ),
    path("dataset/<str:dataset_id>/sync_web", views.Dataset.SyncWeb.as_view()),
    path("dataset/<str:dataset_id>/hit_test", views.Dataset.HitTest.as_view()),
    path(
        "dataset/<str:dataset_id>/document", views.Document.as_view(), name="document"
    ),
    path("dataset/<str:dataset_id>/model", views.Dataset.Model.as_view()),
    path("dataset/document/template/export", views.Template.as_view()),
    path("dataset/document/table_template/export", views.TableTemplate.as_view()),
    path("dataset/<str:dataset_id>/document/web", views.WebDocument.as_view()),
    path("dataset/<str:dataset_id>/document/qa", views.QaDocument.as_view()),
    path("dataset/<str:dataset_id>/document/table", views.TableDocument.as_view()),
    path("dataset/<str:dataset_id>/document/_bach", views.Document.Batch.as_view()),
    path(
        "dataset/<str:dataset_id>/document/batch_hit_handling",
        views.Document.BatchEditHitHandling.as_view(),
    ),
    path(
        "dataset/<str:dataset_id>/document/<int:current_page>/<int:page_size>",
        views.Document.Page.as_view(),
    ),
    path(
        "dataset/<str:dataset_id>/document/batch_refresh",
        views.Document.BatchRefresh.as_view(),
    ),
    path(
        "dataset/<str:dataset_id>/document/batch_generate_related",
        views.Document.BatchGenerateRelated.as_view(),
    ),
    path(
        "dataset/<str:dataset_id>/document/<str:document_id>",
        views.Document.Operate.as_view(),
        name="document_operate",
    ),
    path(
        "dataset/document/split",
        views.Document.Split.as_view(),
        name="document_operate",
    ),
    path(
        "dataset/document/split_pattern",
        views.Document.SplitPattern.as_view(),
        name="document_operate",
    ),
    path(
        "dataset/<str:dataset_id>/document/migrate/<str:target_dataset_id>",
        views.Document.Migrate.as_view(),
    ),
    path(
        "dataset/<str:dataset_id>/document/<str:document_id>/export",
        views.Document.Export.as_view(),
        name="document_export",
    ),
    path(
        "dataset/<str:dataset_id>/document/<str:document_id>/export_zip",
        views.Document.ExportZip.as_view(),
        name="document_export",
    ),
    path(
        "dataset/<str:dataset_id>/document/<str:document_id>/sync",
        views.Document.SyncWeb.as_view(),
    ),
    path(
        "dataset/<str:dataset_id>/document/<str:document_id>/refresh",
        views.Document.Refresh.as_view(),
    ),
    path(
        "dataset/<str:dataset_id>/document/<str:document_id>/cancel_task",
        views.Document.CancelTask.as_view(),
    ),
    path(
        "dataset/<str:dataset_id>/document/cancel_task/_batch",
        views.Document.CancelTask.Batch.as_view(),
    ),
    path(
        "dataset/<str:dataset_id>/document/<str:document_id>/paragraph",
        views.Paragraph.as_view(),
    ),
    path(
        "dataset/<str:dataset_id>/document/batch_generate_related",
        views.Document.BatchGenerateRelated.as_view(),
    ),
    path(
        "dataset/<str:dataset_id>/document/<str:document_id>/paragraph/migrate/dataset/<str:target_dataset_id>/document/<str:target_document_id>",
        views.Paragraph.BatchMigrate.as_view(),
    ),
    path(
        "dataset/<str:dataset_id>/document/<str:document_id>/paragraph/_batch",
        views.Paragraph.Batch.as_view(),
    ),
    path(
        "dataset/<str:dataset_id>/document/<str:document_id>/paragraph/<int:current_page>/<int:page_size>",
        views.Paragraph.Page.as_view(),
        name="paragraph_page",
    ),
    path(
        "dataset/<str:dataset_id>/document/<str:document_id>/paragraph/batch_generate_related",
        views.Paragraph.BatchGenerateRelated.as_view(),
    ),
    path(
        "dataset/<str:dataset_id>/document/<str:document_id>/paragraph/<paragraph_id>",
        views.Paragraph.Operate.as_view(),
    ),
    path(
        "dataset/<str:dataset_id>/document/<str:document_id>/paragraph/<str:paragraph_id>/problem",
        views.Paragraph.Problem.as_view(),
    ),
    path(
        "dataset/<str:dataset_id>/document/<str:document_id>/paragraph/<str:paragraph_id>/problem/<str:problem_id>/un_association",
        views.Paragraph.Problem.UnAssociation.as_view(),
    ),
    path(
        "dataset/<str:dataset_id>/document/<str:document_id>/paragraph/<str:paragraph_id>/problem/<str:problem_id>/association",
        views.Paragraph.Problem.Association.as_view(),
    ),
    path("dataset/<str:dataset_id>/problem", views.Problem.as_view()),
    path(
        "dataset/<str:dataset_id>/problem/_batch", views.Problem.OperateBatch.as_view()
    ),
    path(
        "dataset/<str:dataset_id>/problem/<int:current_page>/<int:page_size>",
        views.Problem.Page.as_view(),
    ),
    path(
        "dataset/<str:dataset_id>/problem/<str:problem_id>",
        views.Problem.Operate.as_view(),
    ),
    path(
        "dataset/<str:dataset_id>/problem/<str:problem_id>/paragraph",
        views.Problem.Paragraph.as_view(),
    ),
    path("image/<str:image_id>", views.Image.Operate.as_view()),
    path("image", views.Image.as_view()),
    path("file/<str:file_id>", views.FileView.Operate.as_view()),
    path("file", views.FileView.as_view()),
]
