.class public final synthetic Lkotlinx/coroutines/time/TimeKt$$ExternalSyntheticApiModelOutline2;
.super Ljava/lang/Object;
.source "D8$$SyntheticClass"


# direct methods
.method public static bridge synthetic m(Ljava/time/Duration;)J
    .registers 3

    .line 0
    invoke-virtual {p0}, Ljava/time/Duration;->toMillis()J

    move-result-wide v0

    return-wide v0
.end method

.method public static bridge synthetic m(Ljava/time/temporal/ChronoUnit;)Ljava/time/Duration;
    .registers 1

    .line 0
    invoke-virtual {p0}, Ljava/time/temporal/ChronoUnit;->getDuration()Ljava/time/Duration;

    move-result-object p0

    return-object p0
.end method

.method public static bridge synthetic m()Ljava/time/temporal/ChronoUnit;
    .registers 1

    .line 0
    sget-object v0, Ljava/time/temporal/ChronoUnit;->MILLIS:Ljava/time/temporal/ChronoUnit;

    return-object v0
.end method
